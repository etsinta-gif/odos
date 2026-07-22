from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from src.core.database import Base, SessionLocal, engine
from src.security.models import SEC_User
from src.transactions.models import ETL_RedFlag


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def _auth_headers(client: TestClient) -> tuple[dict[str, str], str]:
    username = f"alerts_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"AL{uuid4().hex[:6].upper()}",
        "dsa_name": "Alerts Test DSA",
        "username": username,
        "password": password,
    }
    register = client.post("/api/auth/register", json=register_payload)
    assert register.status_code == 200

    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, username


def test_alerts_lifecycle_resolve_and_ignore() -> None:
    db = SessionLocal()
    client = TestClient(app)
    headers, username = _auth_headers(client)

    try:
        user = db.query(SEC_User).filter(SEC_User.username == username).first()
        assert user is not None

        seed = ETL_RedFlag(
            company_id=user.company_id,
            batch_guid="test-alert-batch",
            record_type="commission",
            record_id=101,
            severity="WARNING",
            category="gst",
            message="GST mismatch",
            status="OPEN",
        )
        db.add(seed)
        db.commit()
        db.refresh(seed)

        list_resp = client.get("/api/v1/alerts", headers=headers)
        assert list_resp.status_code == 200
        payload = list_resp.json()
        assert payload["total_records"] >= 1

        summary_resp = client.get("/api/alerts/red-flags/summary", headers=headers)
        assert summary_resp.status_code == 200
        summary_payload = summary_resp.json()
        assert summary_payload["total"] >= 1
        assert "by_status" in summary_payload

        # Seed another tenant row and ensure list stays tenant-scoped.
        other_tenant = ETL_RedFlag(
            company_id=(user.company_id + 999),
            batch_guid="test-alert-batch-other",
            record_type="commission",
            record_id=999,
            severity="CRITICAL",
            category="commission",
            message="Cross-tenant row",
            status="OPEN",
        )
        db.add(other_tenant)
        db.commit()

        scoped_resp = client.get("/api/alerts/red-flags", headers=headers)
        assert scoped_resp.status_code == 200
        scoped_ids = {row["red_flag_id"] for row in scoped_resp.json()["records"]}
        assert seed.red_flag_id in scoped_ids
        assert other_tenant.red_flag_id not in scoped_ids

        resolve_resp = client.put(
            f"/api/alerts/red-flags/{seed.red_flag_id}/resolve",
            json={"status": "OPEN", "resolution_notes": "Validated and approved"},
            headers=headers,
        )
        assert resolve_resp.status_code == 200
        resolve_json = resolve_resp.json()
        assert resolve_json["record"]["status"] == "RESOLVED"
        assert resolve_json["record"]["resolved_by"] is not None
        assert resolve_json["record"]["resolved_at"] is not None

        ignore_resp = client.put(
            f"/api/alerts/red-flags/{seed.red_flag_id}/ignore",
            json={"status": "OPEN", "resolution_notes": "Accepted variance"},
            headers=headers,
        )
        assert ignore_resp.status_code == 200
        ignore_json = ignore_resp.json()
        assert ignore_json["record"]["status"] == "IGNORED"
        assert ignore_json["record"]["resolution_notes"] == "Accepted variance"

    finally:
        db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "test-alert-batch").delete()
        db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "test-alert-batch-other").delete()
        db.commit()
        db.close()
