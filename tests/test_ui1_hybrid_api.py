from uuid import uuid4
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from src.core.database import Base, engine


client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def _register_and_login(prefix: str = "ui1") -> tuple[dict, dict, str]:
    username = f"{prefix}_{uuid4().hex[:8]}"
    password = "Admin@12345"
    register_payload = {
        "dsa_code": f"{prefix[:4].upper()}{uuid4().hex[:6].upper()}",
        "dsa_name": f"{prefix}-tenant",
        "username": username,
        "password": password,
    }
    register_response = client.post("/api/auth/register", json=register_payload)
    assert register_response.status_code == 200

    login_response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert "access_token" in login_payload
    assert "refresh_token" in login_payload

    access_token = login_payload["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    return register_response.json(), headers, login_payload["refresh_token"]


def test_refresh_logout_and_companies_flow() -> None:
    registration, headers, refresh_token = _register_and_login("authflow")

    me_response = client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200

    companies_response = client.get("/api/auth/companies", headers=headers)
    assert companies_response.status_code == 200
    companies = companies_response.json()
    assert len(companies) == 1
    assert companies[0]["company_id"] == registration["company_id"]

    refresh_response = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    refreshed = refresh_response.json()
    assert refreshed["access_token"]
    assert refreshed["refresh_token"]

    logout_response = client.post("/api/auth/logout", headers=headers)
    assert logout_response.status_code == 200
    assert logout_response.json()["revoked_refresh_tokens"] >= 1



def test_dashboard_and_redflags_endpoints() -> None:
    _, headers, _ = _register_and_login("dash")

    stats_response = client.get("/api/masters/dashboard/stats", headers=headers)
    assert stats_response.status_code == 200
    stats_payload = stats_response.json()
    for key in ["lenders", "products", "customers", "cases", "connectors", "revenue", "commission"]:
        assert key in stats_payload

    activities_response = client.get("/api/masters/dashboard/activities", headers=headers)
    assert activities_response.status_code == 200
    assert isinstance(activities_response.json(), list)

    flags_response = client.get("/api/admin/redflags", headers=headers)
    assert flags_response.status_code == 200
    assert isinstance(flags_response.json(), list)



def test_template_resolution_endpoint_requires_auth() -> None:
    response = client.get("/api/v1/etl/template")
    assert response.status_code == 403

    _, headers, _ = _register_and_login("template")
    ok_response = client.get("/api/v1/etl/template", headers=headers)
    assert ok_response.status_code == 200
    payload = ok_response.json()
    assert payload["found"] is False


def test_hybrid_template_match_and_csv_fallback() -> None:
    _, headers, _ = _register_and_login("hybrid")

    template_lookup = client.get(
        "/api/v1/etl/template",
        headers=headers,
        params={"file_name": "TR-01_MIS_TEMPLATE_LenderMaster.xlsx"},
    )
    assert template_lookup.status_code == 200
    lookup_payload = template_lookup.json()
    assert lookup_payload["found"] is True
    assert lookup_payload["resolution"] in {"pattern", "fingerprint"}

    csv_path = Path("samples/_synthetic_phase5/UI1_TEST_UNKNOWN.csv")
    csv_path.write_text("RandomColA,RandomColB\nA1,B1\n", encoding="utf-8")
    with csv_path.open("rb") as f:
        upload_response = client.post(
            "/api/v1/etl/upload",
            headers=headers,
            files={"file": (csv_path.name, f, "text/csv")},
            data={"entity_type": "MST_Lender", "auto_process": "true"},
        )

    assert upload_response.status_code == 200
    upload_payload = upload_response.json()
    assert upload_payload["status"] == "mapping_required"
    assert upload_payload["mode"] == "dynamic_mapping"
    assert upload_payload.get("mapping_required") is True


def test_mapping_draft_submit_activate_flow() -> None:
    _, headers, _ = _register_and_login("mapflow")

    payload = {
        "template_name": f"Draft_{uuid4().hex[:8]}",
        "file_pattern": "UI1_DRAFT_TEST.xlsx",
        "sheet_name": "Sheet1",
        "header_row": 1,
        "mappings": [
            {
                "source_column": "Lender Name",
                "target_table": "MST_Lender",
                "target_field": "lender_name",
                "confidence_score": 90,
                "is_verified": True,
            }
        ],
        "conflict_resolution": "SKIP",
    }

    create_response = client.post("/api/admin/mapping/templates/draft", json=payload, headers=headers)
    assert create_response.status_code == 200
    template_id = create_response.json()["template_id"]

    submit_response = client.post(f"/api/admin/mapping/templates/{template_id}/submit", headers=headers)
    assert submit_response.status_code == 200
    assert submit_response.json()["status"] == "Approved"

    activate_response = client.post(f"/api/admin/mapping/templates/{template_id}/activate", headers=headers)
    assert activate_response.status_code == 200
    assert activate_response.json()["status"] == "Active"
