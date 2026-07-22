from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.alerts.models import ALERT_AuditLog, ALERT_EscalationPolicy, ALERT_Notification, ALERT_Rule
from src.alerts.services.alert_engine import AlertEngine
from src.alerts.services.automation import AutomationEngine
from src.alerts.services.escalation import EscalationEngine
from src.alerts.services.scheduler import scheduler
from src.core.database import get_db
from src.core.tenant import require_company_id
from src.security.auth import get_current_user
from src.security.models import SEC_User
from src.transactions.models import ETL_RedFlag

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)

legacy_router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _role_names(user: SEC_User) -> set[str]:
    return {role.role_name.upper() for role in user.roles}


def _require_any_role(user: SEC_User, allowed: set[str]) -> None:
    if not (_role_names(user) & allowed):
        raise HTTPException(status_code=403, detail="Insufficient permissions")


READ_ROLES = {"ADMIN", "OPS", "FINANCE", "AUDITOR"}
WRITE_ROLES = {"ADMIN", "OPS"}
EXECUTE_ROLES = {"ADMIN", "OPS", "FINANCE"}


class UpdateAlertStatusRequest(BaseModel):
    status: str
    resolution_notes: Optional[str] = None


class RuleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    conditions: dict[str, Any]
    actions: list[dict[str, Any]] = []
    escalation_policy_id: Optional[int] = None
    priority: int = 1


class RuleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    conditions: Optional[dict[str, Any]] = None
    actions: Optional[list[dict[str, Any]]] = None
    escalation_policy_id: Optional[int] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None


class TestRuleRequest(BaseModel):
    red_flag_id: int


class EscalationPolicyCreate(BaseModel):
    name: str
    description: Optional[str] = None
    levels: list[dict[str, Any]]
    default_assignee_role: Optional[str] = None


def _rule_to_dict(rule: ALERT_Rule) -> dict[str, Any]:
    return {
        "rule_id": rule.rule_id,
        "company_id": rule.company_id,
        "name": rule.name,
        "description": rule.description,
        "category": rule.category,
        "conditions": rule.conditions,
        "actions": rule.actions,
        "escalation_policy_id": rule.escalation_policy_id,
        "priority": rule.priority,
        "is_active": rule.is_active,
        "created_by": rule.created_by,
        "created_at": rule.created_at,
        "updated_by": rule.updated_by,
        "updated_at": rule.updated_at,
    }


def _policy_to_dict(policy: ALERT_EscalationPolicy) -> dict[str, Any]:
    return {
        "policy_id": policy.policy_id,
        "company_id": policy.company_id,
        "name": policy.name,
        "description": policy.description,
        "levels": policy.levels,
        "default_assignee_role": policy.default_assignee_role,
        "is_active": policy.is_active,
        "created_by": policy.created_by,
        "created_at": policy.created_at,
        "updated_by": policy.updated_by,
        "updated_at": policy.updated_at,
    }


def _notification_to_dict(notification: ALERT_Notification) -> dict[str, Any]:
    return {
        "notification_id": notification.notification_id,
        "company_id": notification.company_id,
        "rule_id": notification.rule_id,
        "red_flag_id": notification.red_flag_id,
        "type": notification.type,
        "subject": notification.subject,
        "content": notification.content,
        "payload": notification.payload,
        "recipient_user_id": notification.recipient_user_id,
        "recipient_email": notification.recipient_email,
        "sent_at": notification.sent_at,
        "delivered": notification.delivered,
        "error_message": notification.error_message,
        "read": notification.is_read,
        "read_at": notification.read_at,
        "created_at": notification.created_at,
    }


def _audit_to_dict(log: ALERT_AuditLog) -> dict[str, Any]:
    return {
        "log_id": log.log_id,
        "company_id": log.company_id,
        "red_flag_id": log.red_flag_id,
        "rule_id": log.rule_id,
        "action": log.action,
        "details": log.details,
        "performed_by": log.performed_by,
        "performed_at": log.performed_at,
        "ip_address": log.ip_address,
    }


def _query_alerts(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
    status: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
):
    query = db.query(ETL_RedFlag).filter(ETL_RedFlag.company_id == current_user.company_id)

    if status:
        query = query.filter(ETL_RedFlag.status == status.upper())
    if severity:
        query = query.filter(ETL_RedFlag.severity == severity.upper())
    if category:
        query = query.filter(ETL_RedFlag.category == category)

    return query


@router.get("/red-flags")
def list_red_flags(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
    status: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
):
    query = _query_alerts(db, current_user, status, severity, category)

    rows = query.order_by(ETL_RedFlag.created_at.desc()).limit(limit).all()
    return {
        "total_records": len(rows),
        "records": rows,
    }


@router.get("/red-flags/summary")
def red_flags_summary(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    base = db.query(ETL_RedFlag).filter(ETL_RedFlag.company_id == current_user.company_id)
    total = base.count()

    status_rows = (
        db.query(ETL_RedFlag.status, func.count(ETL_RedFlag.red_flag_id))
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .group_by(ETL_RedFlag.status)
        .all()
    )
    severity_rows = (
        db.query(ETL_RedFlag.severity, func.count(ETL_RedFlag.red_flag_id))
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .group_by(ETL_RedFlag.severity)
        .all()
    )
    category_rows = (
        db.query(ETL_RedFlag.category, func.count(ETL_RedFlag.red_flag_id))
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .group_by(ETL_RedFlag.category)
        .all()
    )

    return {
        "total": total,
        "by_status": {k: v for k, v in status_rows},
        "by_severity": {k: v for k, v in severity_rows},
        "by_category": {k: v for k, v in category_rows},
    }


def _update_alert_status(
    red_flag_id: int,
    payload: UpdateAlertStatusRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    allowed = {"OPEN", "RESOLVED", "IGNORED"}
    requested_status = payload.status.upper().strip()
    if requested_status not in allowed:
        raise HTTPException(status_code=400, detail=f"status must be one of: {sorted(allowed)}")

    red_flag = (
        db.query(ETL_RedFlag)
        .filter(ETL_RedFlag.red_flag_id == red_flag_id)
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .first()
    )
    if red_flag is None:
        raise HTTPException(status_code=404, detail="Red flag not found")

    red_flag.status = requested_status
    action = "REOPENED"
    if requested_status in {"RESOLVED", "IGNORED"}:
        red_flag.resolution_notes = payload.resolution_notes
        red_flag.resolved_by = current_user.user_id
        red_flag.resolved_at = datetime.utcnow()
        action = requested_status
    else:
        red_flag.resolution_notes = None
        red_flag.resolved_by = None
        red_flag.resolved_at = None

    db.add(
        ALERT_AuditLog(
            company_id=current_user.company_id,
            red_flag_id=red_flag.red_flag_id,
            action=action,
            details={"resolution_notes": payload.resolution_notes},
            performed_by=current_user.user_id,
            performed_at=datetime.utcnow(),
        )
    )
    db.commit()
    db.refresh(red_flag)
    return {
        "message": "Alert status updated",
        "record": red_flag,
    }


@router.put("/red-flags/{red_flag_id}/resolve")
def resolve_red_flag(
    red_flag_id: int,
    payload: UpdateAlertStatusRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    payload.status = "RESOLVED"
    return _update_alert_status(red_flag_id, payload, db, current_user)


@router.put("/red-flags/{red_flag_id}/ignore")
def ignore_red_flag(
    red_flag_id: int,
    payload: UpdateAlertStatusRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    payload.status = "IGNORED"
    return _update_alert_status(red_flag_id, payload, db, current_user)


@router.get("/rules")
def list_rules(
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, READ_ROLES)
    query = db.query(ALERT_Rule).filter(ALERT_Rule.company_id == current_user.company_id)

    if category:
        query = query.filter(ALERT_Rule.category == category)
    if is_active is not None:
        query = query.filter(ALERT_Rule.is_active == is_active)

    return [_rule_to_dict(rule) for rule in query.order_by(ALERT_Rule.rule_id.desc()).all()]


@router.get("/rules/{rule_id}")
def get_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, READ_ROLES)
    rule = (
        db.query(ALERT_Rule)
        .filter(ALERT_Rule.rule_id == rule_id)
        .filter(ALERT_Rule.company_id == current_user.company_id)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return _rule_to_dict(rule)


@router.post("/rules")
def create_rule(
    rule_data: RuleCreate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, WRITE_ROLES)
    rule = ALERT_Rule(
        company_id=current_user.company_id,
        name=rule_data.name,
        description=rule_data.description,
        category=rule_data.category,
        conditions=rule_data.conditions,
        actions=rule_data.actions,
        escalation_policy_id=rule_data.escalation_policy_id,
        priority=rule_data.priority,
        is_active=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)
    return {"rule_id": rule.rule_id, "message": "Rule created successfully"}


@router.put("/rules/{rule_id}")
def update_rule(
    rule_id: int,
    rule_data: RuleUpdate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, WRITE_ROLES)
    rule = (
        db.query(ALERT_Rule)
        .filter(ALERT_Rule.rule_id == rule_id)
        .filter(ALERT_Rule.company_id == current_user.company_id)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    for field, value in rule_data.model_dump(exclude_unset=True).items():
        setattr(rule, field, value)

    rule.updated_by = current_user.user_id
    db.commit()

    return {"message": "Rule updated successfully"}


@router.delete("/rules/{rule_id}")
def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, WRITE_ROLES)
    rule = (
        db.query(ALERT_Rule)
        .filter(ALERT_Rule.rule_id == rule_id)
        .filter(ALERT_Rule.company_id == current_user.company_id)
        .first()
    )
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    rule.is_active = False
    rule.updated_by = current_user.user_id
    db.commit()

    return {"message": "Rule deleted successfully"}


@router.post("/rules/{rule_id}/test")
def test_rule(
    rule_id: int,
    payload: TestRuleRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, EXECUTE_ROLES)

    rule = (
        db.query(ALERT_Rule)
        .filter(ALERT_Rule.rule_id == rule_id)
        .filter(ALERT_Rule.company_id == current_user.company_id)
        .first()
    )

    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    red_flag = (
        db.query(ETL_RedFlag)
        .filter(ETL_RedFlag.red_flag_id == payload.red_flag_id)
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .first()
    )

    if not red_flag:
        raise HTTPException(status_code=404, detail="Red flag not found")

    engine = AlertEngine(db, current_user.company_id)
    return engine.evaluate_rule(rule, red_flag, actor_user_id=current_user.user_id)


@router.post("/red-flags/{red_flag_id}/evaluate")
def evaluate_red_flag_against_all_rules(
    red_flag_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, EXECUTE_ROLES)

    red_flag = (
        db.query(ETL_RedFlag)
        .filter(ETL_RedFlag.red_flag_id == red_flag_id)
        .filter(ETL_RedFlag.company_id == current_user.company_id)
        .first()
    )
    if not red_flag:
        raise HTTPException(status_code=404, detail="Red flag not found")

    engine = AlertEngine(db, current_user.company_id)
    results = engine.evaluate_all_rules(red_flag, actor_user_id=current_user.user_id)
    return {"triggered": len(results), "results": results}


@router.get("/escalation-policies")
def list_escalation_policies(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, READ_ROLES)
    rows = (
        db.query(ALERT_EscalationPolicy)
        .filter(ALERT_EscalationPolicy.company_id == current_user.company_id)
        .order_by(ALERT_EscalationPolicy.policy_id.desc())
        .all()
    )
    return [_policy_to_dict(row) for row in rows]


@router.post("/escalation-policies")
def create_escalation_policy(
    payload: EscalationPolicyCreate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, WRITE_ROLES)
    row = ALERT_EscalationPolicy(
        company_id=current_user.company_id,
        name=payload.name,
        description=payload.description,
        levels=payload.levels,
        default_assignee_role=payload.default_assignee_role,
        is_active=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {"policy_id": row.policy_id, "message": "Escalation policy created"}


@router.get("/notifications")
def get_notifications(
    limit: int = Query(50, ge=1, le=500),
    read: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, READ_ROLES)

    query = db.query(ALERT_Notification).filter(
        ALERT_Notification.company_id == current_user.company_id,
        (ALERT_Notification.recipient_user_id == current_user.user_id)
        | (ALERT_Notification.recipient_email == current_user.email),
    )

    if read is not None:
        query = query.filter(ALERT_Notification.is_read == read)

    rows = query.order_by(ALERT_Notification.sent_at.desc()).limit(limit).all()
    return [_notification_to_dict(row) for row in rows]


@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, WRITE_ROLES)

    notification = (
        db.query(ALERT_Notification)
        .filter(ALERT_Notification.notification_id == notification_id)
        .filter(ALERT_Notification.company_id == current_user.company_id)
        .first()
    )

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()

    return {"message": "Notification marked as read"}


@router.get("/audit")
def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    action: Optional[str] = None,
    red_flag_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, READ_ROLES)
    query = db.query(ALERT_AuditLog).filter(ALERT_AuditLog.company_id == current_user.company_id)

    if action:
        query = query.filter(ALERT_AuditLog.action == action.upper())
    if red_flag_id:
        query = query.filter(ALERT_AuditLog.red_flag_id == red_flag_id)

    rows = query.order_by(ALERT_AuditLog.performed_at.desc()).limit(limit).all()
    return [_audit_to_dict(row) for row in rows]


@router.post("/automation/auto-resolve")
def run_auto_resolve(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, EXECUTE_ROLES)
    engine = AutomationEngine(db, current_user.company_id)
    return engine.auto_resolve_low_severity()


@router.post("/automation/check-escalations")
def check_escalations(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, EXECUTE_ROLES)
    engine = EscalationEngine(db, current_user.company_id)
    result = engine.check_escalations()
    return {"escalated": len(result), "details": result}


@router.post("/scheduler/run-once")
def run_alert_scheduler_once(
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})
    return {
        "rules": scheduler.run_rule_checks_once(),
        "escalations": scheduler.run_escalations_once(),
        "auto_resolve": scheduler.run_auto_resolve_once(),
    }


@legacy_router.get("")
def list_alerts_legacy(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
    status: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
):
    return list_red_flags(db, current_user, status, severity, category, limit)


@legacy_router.patch("/{red_flag_id}")
def update_alert_status_legacy(
    red_flag_id: int,
    payload: UpdateAlertStatusRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    return _update_alert_status(red_flag_id, payload, db, current_user)
