from datetime import date, datetime
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app, startup_event
from src.bi.models import BI_DashboardDefinition, BI_ReportDefinition, BI_WidgetDefinition
from src.core.database import Base, SessionLocal, engine
from src.masters.models import MST_DSA
from src.security.auth import get_password_hash
from src.security.models import SEC_Role, SEC_User
from src.transactions.models import ETL_RedFlag, TRN_Revenue


client = TestClient(app)


def setup_module(module):
    startup_event()
    Base.metadata.create_all(bind=engine)


def _register_and_login(prefix: str = "bi") -> tuple[dict, str]:
    username = f"{prefix}_{uuid4().hex[:8]}"
    password = "Admin@12345"
    payload = {
        "dsa_code": f"{prefix[:3].upper()}{uuid4().hex[:6].upper()}",
        "dsa_name": f"{prefix}-tenant",
        "username": username,
        "password": password,
    }
    reg = client.post("/api/auth/register", json=payload)
    assert reg.status_code == 200

    login = client.post("/api/auth/login", json={"username": username, "password": password})
    assert login.status_code == 200
    token = login.json()["access_token"]
    return reg.json(), token


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _seed_bi_data(db: Session, company_id: int) -> None:
    rows = [
        TRN_Revenue(
            company_id=company_id,
            revenue_date=date.today(),
            net_amount=100,
            reported_amount=100,
            reported_gst=18,
            reported_tds=2,
            system_gst=18,
            system_tds=2,
            gst_match=True,
            tds_match=True,
            data={"lender_name": "HDFC", "commission_rate": 2.5},
            is_active=True,
        ),
        TRN_Revenue(
            company_id=company_id,
            revenue_date=date.today(),
            net_amount=200,
            reported_amount=200,
            reported_gst=20,
            reported_tds=2,
            system_gst=36,
            system_tds=4,
            gst_match=False,
            tds_match=False,
            data={"lender_name": "ICICI", "commission_rate": 3.5},
            is_active=True,
        ),
    ]
    db.add_all(rows)
    db.add(
        ETL_RedFlag(
            company_id=company_id,
            batch_guid="bi-test",
            record_type="revenue",
            record_id=1,
            severity="WARNING",
            category="gst",
            message="GST mismatch",
            status="OPEN",
        )
    )
    db.commit()


def test_bi_crud_execute_export_trends_dashboard() -> None:
    reg, token = _register_and_login("bi_flow")
    headers = _auth_headers(token)

    db = SessionLocal()
    _seed_bi_data(db, reg["company_id"])
    db.close()

    create_payload = {
        "name": "Revenue by GST Match",
        "description": "BI report",
        "category": "Financial",
        "output_format": "HTML",
        "definition": {
            "source": "TRN_Revenue",
            "dimensions": ["gst_match"],
            "metrics": [{"field": "reported_amount", "aggregation": "sum", "alias": "total_revenue"}],
            "filters": [],
            "order_by": [{"field": "total_revenue", "direction": "desc"}],
            "limit": 50,
        },
        "is_public": False,
    }
    create_resp = client.post("/api/bi/reports/", json=create_payload, headers=headers)
    assert create_resp.status_code == 200
    report_id = create_resp.json()["report_id"]

    list_resp = client.get("/api/bi/reports/", headers=headers)
    assert list_resp.status_code == 200
    assert any(item["report_id"] == report_id for item in list_resp.json())

    get_resp = client.get(f"/api/bi/reports/{report_id}", headers=headers)
    assert get_resp.status_code == 200

    update_resp = client.put(
        f"/api/bi/reports/{report_id}",
        json={"name": "Revenue by GST Match v2"},
        headers=headers,
    )
    assert update_resp.status_code == 200

    exec_resp = client.post(f"/api/bi/reports/{report_id}/execute", headers=headers)
    assert exec_resp.status_code == 200
    exec_payload = exec_resp.json()
    assert "columns" in exec_payload and "data" in exec_payload

    jsonb_report = {
        "name": "JSON Dimension Report",
        "description": "JSON path report",
        "category": "Custom",
        "output_format": "HTML",
        "definition": {
            "source": "TRN_Revenue",
            "dimensions": ["data.lender_name"],
            "metrics": [{"field": "data.commission_rate", "aggregation": "avg", "alias": "avg_rate"}],
            "filters": [],
        },
        "is_public": False,
    }
    json_resp = client.post("/api/bi/reports/", json=jsonb_report, headers=headers)
    assert json_resp.status_code == 200
    json_report_id = json_resp.json()["report_id"]

    json_exec = client.post(f"/api/bi/reports/{json_report_id}/execute", headers=headers)
    assert json_exec.status_code == 200
    assert any("data.lender_name" == col for col in json_exec.json()["columns"])

    pdf_resp = client.get(f"/api/bi/reports/{report_id}/export/pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"].startswith("application/pdf") or pdf_resp.headers["content-type"].startswith("application/octet-stream")

    excel_resp = client.get(f"/api/bi/reports/{report_id}/export/excel", headers=headers)
    assert excel_resp.status_code == 200
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in excel_resp.headers["content-type"]

    csv_resp = client.get(f"/api/bi/reports/{report_id}/export/csv", headers=headers)
    assert csv_resp.status_code == 200
    assert csv_resp.headers["content-type"].startswith("text/csv")

    trend_resp = client.get("/api/bi/trends/gst_mismatch?days=30", headers=headers)
    assert trend_resp.status_code == 200
    assert trend_resp.json()["metric"] == "gst_mismatch"

    summary_resp = client.get("/api/bi/trends/summary", headers=headers)
    assert summary_resp.status_code == 200
    summary_payload = summary_resp.json()
    assert "gst_mismatches" in summary_payload and "red_flags" in summary_payload

    dash_resp = client.post(
        "/api/bi/dashboards/",
        json={"name": "Main Dashboard", "description": "BI dash", "layout": {"cols": 12}},
        headers=headers,
    )
    assert dash_resp.status_code == 200
    dashboard_id = dash_resp.json()["dashboard_id"]

    widget_resp = client.post(
        f"/api/bi/dashboards/{dashboard_id}/widgets",
        json={
            "title": "Revenue Widget",
            "type": "CHART",
            "chart_type": "BAR",
            "report_id": report_id,
            "width": 6,
            "height": 4,
        },
        headers=headers,
    )
    assert widget_resp.status_code == 200
    widget_id = widget_resp.json()["widget_id"]

    get_dash_resp = client.get(f"/api/bi/dashboards/{dashboard_id}", headers=headers)
    assert get_dash_resp.status_code == 200
    assert any(w["widget_id"] == widget_id for w in get_dash_resp.json()["widgets"])

    run_widget = client.post(f"/api/bi/dashboards/{dashboard_id}/widgets/{widget_id}/execute", headers=headers)
    assert run_widget.status_code == 200
    assert "data" in run_widget.json()

    schedule_resp = client.post(
        f"/api/bi/reports/{report_id}/schedule",
        json={"frequency": "daily", "time": "09:00", "recipients": ["ops@example.com"]},
        headers=headers,
    )
    assert schedule_resp.status_code == 200

    delete_dash = client.delete(f"/api/bi/dashboards/{dashboard_id}", headers=headers)
    assert delete_dash.status_code == 200

    delete_report = client.delete(f"/api/bi/reports/{report_id}", headers=headers)
    assert delete_report.status_code == 200


def test_bi_permissions() -> None:
    # Unauthenticated should be blocked.
    no_auth = client.get("/api/bi/reports/")
    assert no_auth.status_code in {401, 403}

    reg, _ = _register_and_login("bi_ops")
    company_id = reg["company_id"]

    db = SessionLocal()
    try:
        ops_role = db.query(SEC_Role).filter(SEC_Role.role_name == "OPS").first()
        if ops_role is None:
            ops_role = SEC_Role(role_name="OPS", description="Ops", is_system=False)
            db.add(ops_role)
            db.flush()

        dsa = MST_DSA(
            dsa_code=f"OPS{uuid4().hex[:6].upper()}",
            dsa_name="ops-company",
            is_active=True,
        )
        db.add(dsa)
        db.flush()

        user = SEC_User(
            company_id=dsa.dsa_id,
            username=f"ops_user_{uuid4().hex[:6]}",
            password_hash=get_password_hash("Admin@12345"),
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        user.roles.append(ops_role)
        db.add(user)
        db.commit()

        login = client.post("/api/auth/login", json={"username": user.username, "password": "Admin@12345"})
        assert login.status_code == 200
        ops_headers = _auth_headers(login.json()["access_token"])

        denied = client.get("/api/bi/reports/", headers=ops_headers)
        assert denied.status_code == 403

    finally:
        # soft cleanup on test tenant data
        db.close()
