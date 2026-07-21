from contextvars import ContextVar
from typing import Optional

from fastapi import Depends, HTTPException, status

from src.security.auth import get_current_user

_current_company_id: ContextVar[Optional[int]] = ContextVar("current_company_id", default=None)


def set_current_company_id(company_id: Optional[int]) -> None:
    _current_company_id.set(company_id)


def get_current_company_id() -> Optional[int]:
    return _current_company_id.get()


def require_company_id(current_user=Depends(get_current_user)) -> int:
    company_id = getattr(current_user, "company_id", None)
    if company_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authenticated user is not bound to a company",
        )
    set_current_company_id(company_id)
    return company_id
