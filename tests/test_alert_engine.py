from datetime import datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app, startup_event
from src.alerts.models import ALERT_AuditLog, ALERT_EscalationPolicy, ALERT_Rule
from src.core.database import Base, SessionLocal, engine
from src.security.auth import get_password_hash
from src.security.models import SEC_Role, SEC_User
from src.transactions.models import ETL_RedFlag


client = TestClient(app)


def setup_module(module):
    startup_event()
    Base.metadata.create_all(bind=engine)


def _register_and_login(prefix: str = "alert") -> tuple[dict, str]:
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


def test_alert_rule_crud_trigger_notification_and_audit() -> None:
    reg, token = _register_and_login("alert_flow")
    headers = _auth_headers(token)

    db = SessionLocal()
    try:
        admin = db.query(SEC_User).filter(SEC_User.company_id == reg["company_id"]).first()
        assert admin is not None

        red_flag = ETL_RedFlag(
            company_id=reg["company_id"],
            batch_guid="int3-test",
            record_type="revenue",
            record_id=901,
            severity="WARNING",
            category="GST_MISMATCH",
            message="GST mismatch for rule evaluation",
            status="OPEN",
        )
        db.add(red_flag)
        db.commit()
        db.refresh(red_flag)

        policy_resp = client.post(
            "/api/alerts/escalation-policies",
            json={
                "name": "Standard Escalation",
                "description": "Escalate in 60 mins",
                "levels": [{"level": 1, "time_minutes": 60, "assign_to_role": "ADMIN"}],
                "default_assignee_role": "ADMIN",
            },
            headers=headers,
        )
        assert policy_resp.status_code == 200
        policy_id = policy_resp.json()["policy_id"]

        create_rule = client.post(
            "/api/alerts/rules",
            json={
                "name": "GST Warning Rule",
                "description": "Trigger on GST category warning",
                "category": "GST_MISMATCH",
                "conditions": {"field": "severity", "operator": "eq", "value": "WARNING"},
                "actions": [{"type": "in_app", "config": {"user_ids": [admin.user_id], "subject": "Rule Hit"}}],
                "escalation_policy_id": policy_id,
                "priority": 2,
            },
            headers=headers,
        )
        assert create_rule.status_code == 200
        rule_id = create_rule.json()["rule_id"]

        list_rules = client.get("/api/alerts/rules", headers=headers)
        assert list_rules.status_code == 200
        assert any(rule["rule_id"] == rule_id for rule in list_rules.json())

        get_rule = client.get(f"/api/alerts/rules/{rule_id}", headers=headers)
        assert get_rule.status_code == 200
        assert get_rule.json()["name"] == "GST Warning Rule"

        update_rule = client.put(
            f"/api/alerts/rules/{rule_id}",
            json={"priority": 3},
            headers=headers,
        )
        assert update_rule.status_code == 200

        test_rule = client.post(
            f"/api/alerts/rules/{rule_id}/test",
            json={"red_flag_id": red_flag.red_flag_id},
            headers=headers,
        )
        assert test_rule.status_code == 200
        assert test_rule.json()["triggered"] is True

        notifications = client.get("/api/alerts/notifications", headers=headers)
        assert notifications.status_code == 200
        notif_rows = notifications.json()
        assert len(notif_rows) >= 1
        notification_id = notif_rows[0]["notification_id"]

        mark_read = client.put(f"/api/alerts/notifications/{notification_id}/read", headers=headers)
        assert mark_read.status_code == 200

        audit = client.get("/api/alerts/audit", headers=headers)
        assert audit.status_code == 200
        assert any(item["action"] == "TRIGGERED" for item in audit.json())

        delete_rule = client.delete(f"/api/alerts/rules/{rule_id}", headers=headers)
        assert delete_rule.status_code == 200

    finally:
        db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "int3-test").delete()
        db.query(ALERT_AuditLog).filter(ALERT_AuditLog.company_id == reg["company_id"]).delete()
        db.query(ALERT_Rule).filter(ALERT_Rule.company_id == reg["company_id"]).delete()
        db.query(ALERT_EscalationPolicy).filter(ALERT_EscalationPolicy.company_id == reg["company_id"]).delete()
        db.commit()
        db.close()


def test_alert_permissions_and_automation() -> None:
    unauth = client.get("/api/alerts/rules")
    assert unauth.status_code in {401, 403}

    reg, token = _register_and_login("alert_perm")
    headers = _auth_headers(token)

    db = SessionLocal()
    try:
        info_flag = ETL_RedFlag(
            company_id=reg["company_id"],
            batch_guid="int3-auto",
            record_type="commission",
            record_id=902,
            severity="INFO",
            category="TDS_MISMATCH",
            message="Low severity for auto-resolve",
            status="OPEN",
        )
        old_flag = ETL_RedFlag(
            company_id=reg["company_id"],
            batch_guid="int3-auto",
            record_type="commission",
            record_id=903,
            severity="WARNING",
            category="TDS_MISMATCH",
            message="Old open flag",
            status="OPEN",
            created_at=datetime.utcnow() - timedelta(days=2),
        )
        db.add_all([info_flag, old_flag])
        db.commit()

        auto_resolve = client.post("/api/alerts/automation/auto-resolve", headers=headers)
        assert auto_resolve.status_code == 200
        assert auto_resolve.json()["resolved"] >= 1

        policy_resp = client.post(
            "/api/alerts/escalation-policies",
            json={"name": "Esc Fast", "levels": [{"level": 1, "time_minutes": 30, "assign_to_role": "ADMIN"}]},
            headers=headers,
        )
        assert policy_resp.status_code == 200

        escalations = client.post("/api/alerts/automation/check-escalations", headers=headers)
        assert escalations.status_code == 200
        assert escalations.json()["escalated"] >= 1

        role = db.query(SEC_Role).filter(SEC_Role.role_name == "VIEWER").first()
        if role is None:
            role = SEC_Role(role_name="VIEWER", description="Read-only viewer", is_system=False)
            db.add(role)
            db.flush()

        viewer = SEC_User(
            company_id=reg["company_id"],
            username=f"viewer_{uuid4().hex[:6]}",
            password_hash=get_password_hash("Admin@12345"),
            is_active=True,
        )
        viewer.roles.append(role)
        db.add(viewer)
        db.commit()

        viewer_login = client.post("/api/auth/login", json={"username": viewer.username, "password": "Admin@12345"})
        assert viewer_login.status_code == 200
        viewer_headers = _auth_headers(viewer_login.json()["access_token"])

        denied = client.get("/api/alerts/rules", headers=viewer_headers)
        assert denied.status_code == 403

    finally:
        db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "int3-auto").delete()
        db.query(ALERT_AuditLog).filter(ALERT_AuditLog.company_id == reg["company_id"]).delete()
        db.query(ALERT_Rule).filter(ALERT_Rule.company_id == reg["company_id"]).delete()
        db.query(ALERT_EscalationPolicy).filter(ALERT_EscalationPolicy.company_id == reg["company_id"]).delete()
        db.commit()
        db.close()
