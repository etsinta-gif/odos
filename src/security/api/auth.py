from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.masters.models import MST_DSA
from src.security.auth import (
    authenticate_user,
    create_access_token,
    exchange_refresh_token,
    get_current_user,
    get_password_hash,
    issue_refresh_token,
    revoke_all_refresh_tokens_for_user,
    revoke_refresh_token,
)
from src.security.models import SEC_Role, SEC_User

router = APIRouter(prefix="/api/auth", tags=["security"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RegisterRequest(BaseModel):
    dsa_code: str = Field(min_length=1)
    dsa_name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str = Field(min_length=8)
    email: str | None = None
    full_name: str | None = None


class RegisterResponse(BaseModel):
    user_id: int
    company_id: int
    dsa_id: int
    username: str


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=8)


class LogoutRequest(BaseModel):
    refresh_token: str | None = None


class CompanySummary(BaseModel):
    company_id: int
    company_code: str
    company_name: str


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    username = ""
    password = ""

    content_type = (request.headers.get("content-type") or "").lower()
    if "application/json" in content_type:
        payload = LoginRequest(**(await request.json()))
        username = payload.username
        password = payload.password
    else:
        form = await request.form()
        username = str(form.get("username") or "").strip()
        password = str(form.get("password") or "")
        if not username or not password:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username and password are required")

    source_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    user = authenticate_user(db, username, password, source_ip=source_ip, user_agent=user_agent)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(
        {
            "sub": user.username,
            "company_id": user.company_id,
            "roles": [role.role_name for role in user.roles],
        }
    )
    refresh_token = issue_refresh_token(db, user)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    user = exchange_refresh_token(db, payload.refresh_token)
    new_access_token = create_access_token(
        {
            "sub": user.username,
            "company_id": user.company_id,
            "roles": [role.role_name for role in user.roles],
        }
    )
    new_refresh_token = getattr(user, "_issued_refresh_token", None)
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}


@router.post("/logout")
def logout(
    payload: LogoutRequest | None = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    revoked = 0
    if payload and payload.refresh_token:
        revoked = 1 if revoke_refresh_token(db, payload.refresh_token) else 0
    else:
        revoked = revoke_all_refresh_tokens_for_user(db, current_user.user_id)
    return {"message": "Logged out", "revoked_refresh_tokens": revoked}


@router.post("/register", response_model=RegisterResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(MST_DSA).filter(MST_DSA.dsa_code == payload.dsa_code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DSA code already exists")

    if db.query(SEC_User).filter(SEC_User.username == payload.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    admin_role = db.query(SEC_Role).filter(SEC_Role.role_name == "ADMIN").first()
    if not admin_role:
        admin_role = SEC_Role(role_name="ADMIN", description="System admin", is_system=True)
        db.add(admin_role)
        db.flush()

    dsa = MST_DSA(
        dsa_code=payload.dsa_code,
        dsa_name=payload.dsa_name,
        is_active=True,
    )
    db.add(dsa)
    db.flush()

    user = SEC_User(
        company_id=dsa.dsa_id,
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        is_active=True,
    )
    user.roles.append(admin_role)
    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterResponse(
        user_id=user.user_id,
        company_id=user.company_id,
        dsa_id=dsa.dsa_id,
        username=user.username,
    )


@router.get("/me")
def me(current_user: SEC_User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "company_id": current_user.company_id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "is_active": current_user.is_active,
        "roles": [role.role_name for role in current_user.roles],
    }


@router.get("/companies", response_model=list[CompanySummary])
def companies(current_user: SEC_User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Current security model binds users to one company; return that company for UI tenant context.
    company = db.query(MST_DSA).filter(MST_DSA.dsa_id == current_user.company_id, MST_DSA.is_active == True).first()
    if not company:
        return []
    return [
        CompanySummary(
            company_id=company.dsa_id,
            company_code=company.dsa_code,
            company_name=company.dsa_name,
        )
    ]
