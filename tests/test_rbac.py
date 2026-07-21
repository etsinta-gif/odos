from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from src.security.auth import create_access_token, require_role


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "admin", "company_id": 1, "roles": ["ADMIN"]})
    assert isinstance(token, str)
    assert token


def test_require_role_allows_user_with_matching_role():
    user = SimpleNamespace(roles=[SimpleNamespace(role_name="OPS")])

    @require_role(["OPS", "ADMIN"])
    def endpoint(*, current_user):
        return {"ok": True}

    result = endpoint(current_user=user)
    assert result["ok"] is True


def test_require_role_blocks_user_without_required_role():
    user = SimpleNamespace(roles=[SimpleNamespace(role_name="AUDITOR")])

    @require_role(["ADMIN"])
    def endpoint(*, current_user):
        return {"ok": True}

    with pytest.raises(HTTPException) as exc:
        endpoint(current_user=user)
    assert exc.value.status_code == 403
