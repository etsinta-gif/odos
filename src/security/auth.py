import os
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.security.models import SEC_LoginHistory, SEC_RefreshToken, SEC_User

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer(auto_error=True)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _utcnow_naive() -> datetime:
    # SQLAlchemy models in this project use UTC naive datetimes.
    return datetime.utcnow()


def _hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issue_refresh_token(db: Session, user: SEC_User) -> str:
    raw_token = secrets.token_urlsafe(48)
    expires_at = _utcnow_naive() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token_row = SEC_RefreshToken(
        user_id=user.user_id,
        token_hash=_hash_refresh_token(raw_token),
        issued_at=_utcnow_naive(),
        expires_at=expires_at,
    )
    db.add(token_row)
    db.commit()
    return raw_token


def revoke_refresh_token(db: Session, raw_token: str) -> bool:
    token_hash = _hash_refresh_token(raw_token)
    row = db.query(SEC_RefreshToken).filter(SEC_RefreshToken.token_hash == token_hash).first()
    if not row or row.revoked_at is not None:
        return False
    row.revoked_at = _utcnow_naive()
    db.commit()
    return True


def revoke_all_refresh_tokens_for_user(db: Session, user_id: int) -> int:
    rows = (
        db.query(SEC_RefreshToken)
        .filter(SEC_RefreshToken.user_id == user_id)
        .filter(SEC_RefreshToken.revoked_at == None)
        .all()
    )
    now = _utcnow_naive()
    for row in rows:
        row.revoked_at = now
    if rows:
        db.commit()
    return len(rows)


def exchange_refresh_token(db: Session, raw_token: str) -> SEC_User:
    token_hash = _hash_refresh_token(raw_token)
    row = db.query(SEC_RefreshToken).filter(SEC_RefreshToken.token_hash == token_hash).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    if row.revoked_at is not None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token revoked")
    if row.expires_at <= _utcnow_naive():
        row.revoked_at = _utcnow_naive()
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")

    user = db.query(SEC_User).filter(SEC_User.user_id == row.user_id, SEC_User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    # Rotate refresh token on every exchange.
    new_raw = secrets.token_urlsafe(48)
    new_hash = _hash_refresh_token(new_raw)
    row.revoked_at = _utcnow_naive()
    row.replaced_by_hash = new_hash

    db.add(
        SEC_RefreshToken(
            user_id=user.user_id,
            token_hash=new_hash,
            issued_at=_utcnow_naive(),
            expires_at=_utcnow_naive() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )
    )
    db.commit()
    setattr(user, "_issued_refresh_token", new_raw)
    return user


def _log_login_attempt(
    db: Session,
    *,
    user: SEC_User | None,
    username: str,
    auth_status: str,
    source_ip: str | None,
    user_agent: str | None,
    failure_reason: str | None = None,
) -> None:
    history = SEC_LoginHistory(
        user_id=user.user_id if user else None,
        company_id=user.company_id if user else 0,
        username=username,
        login_at=datetime.utcnow(),
        auth_status=auth_status,
        source_ip=source_ip,
        user_agent=user_agent,
        failure_reason=failure_reason,
    )
    db.add(history)
    try:
        db.commit()
    except Exception:
        db.rollback()


def authenticate_user(
    db: Session,
    username: str,
    password: str,
    source_ip: str | None = None,
    user_agent: str | None = None,
) -> SEC_User | None:
    user = db.query(SEC_User).filter(SEC_User.username == username, SEC_User.is_active == True).first()
    if not user:
        _log_login_attempt(
            db,
            user=None,
            username=username,
            auth_status="FAILED",
            source_ip=source_ip,
            user_agent=user_agent,
            failure_reason="USER_NOT_FOUND",
        )
        return None
    if not verify_password(password, user.password_hash):
        _log_login_attempt(
            db,
            user=user,
            username=username,
            auth_status="FAILED",
            source_ip=source_ip,
            user_agent=user_agent,
            failure_reason="INVALID_PASSWORD",
        )
        return None
    user.last_login = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)
    _log_login_attempt(
        db,
        user=user,
        username=username,
        auth_status="SUCCESS",
        source_ip=source_ip,
        user_agent=user_agent,
    )
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> SEC_User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = db.query(SEC_User).filter(SEC_User.username == username, SEC_User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_role(allowed_roles: Iterable[str]) -> Callable:
    allowed = {role.upper() for role in allowed_roles}

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Missing current_user dependency",
                )
            user_roles = {role.role_name.upper() for role in user.roles}
            if not (user_roles & allowed):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
            return func(*args, **kwargs)

        return wrapper

    return decorator
