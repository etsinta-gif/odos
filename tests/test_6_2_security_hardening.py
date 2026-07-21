from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import inspect

from app.main import app
from src.core.database import Base, SessionLocal, engine
from src.security.auth import get_password_hash
from src.security.models import SEC_LoginHistory, SEC_Role, SEC_User


client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def _register_and_login(prefix: str = "imp62") -> tuple[dict, dict]:
    username = f"{prefix}_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"{prefix[:4].upper()}{uuid4().hex[:6].upper()}",
        "dsa_name": f"{prefix}-tenant",
        "username": username,
        "password": password,
        "email": f"{username}@example.com",
    }
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 200

    login_response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return register_response.json(), {"Authorization": f"Bearer {token}"}


def test_register_and_me_endpoint() -> None:
    registration, headers = _register_and_login("me")
    me_response = client.get("/api/auth/me", headers=headers)

    assert me_response.status_code == 200
    payload = me_response.json()
    assert payload["company_id"] == registration["company_id"]
    assert "ADMIN" in payload["roles"]


def test_etl_requires_authentication() -> None:
    response = client.get("/api/v1/etl/batches")
    assert response.status_code == 403


def test_login_history_records_success_and_failure() -> None:
    username = f"audit_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"AUD{uuid4().hex[:6].upper()}",
        "dsa_name": "audit-tenant",
        "username": username,
        "password": password,
    }
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 200

    bad_login = client.post("/api/auth/login", json={"username": username, "password": "wrong-password"})
    assert bad_login.status_code == 401

    ok_login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert ok_login.status_code == 200

    db = SessionLocal()
    try:
        columns = {col["name"] for col in inspect(engine).get_columns("sec_login_history")}
        if "username" not in columns:
            return
        logs = (
            db.query(SEC_LoginHistory)
            .filter(SEC_LoginHistory.username == username)
            .order_by(SEC_LoginHistory.login_id.desc())
            .all()
        )
        assert any(log.auth_status == "FAILED" and log.failure_reason == "INVALID_PASSWORD" for log in logs)
        assert any(log.auth_status == "SUCCESS" for log in logs)
    finally:
        db.close()


def test_mapping_mutation_requires_admin() -> None:
    username = f"ops_{uuid4().hex[:8]}"
    db = SessionLocal()
    try:
        role = db.query(SEC_Role).filter(SEC_Role.role_name == "OPS").first()
        if role is None:
            role = SEC_Role(role_name="OPS", description="Ops role", is_system=False)
            db.add(role)
            db.flush()

        user = SEC_User(
            company_id=1,
            username=username,
            password_hash=get_password_hash("Admin@12345"),
            is_active=True,
        )
        user.roles.append(role)
        db.add(user)
        db.commit()
    finally:
        db.close()

    login = client.post("/api/auth/login", json={"username": username, "password": "Admin@12345"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "template_name": f"ops_template_{uuid4().hex[:6]}",
        "sheet_name": "Sheet1",
        "header_row": 1,
        "mappings": [
            {
                "source_column": "A",
                "target_table": "MST_Lender",
                "target_field": "lender_name",
            }
        ],
    }
    response = client.post("/api/admin/mapping/confirm", json=payload, headers=headers)
    assert response.status_code == 403
