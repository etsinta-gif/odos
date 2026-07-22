from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from src.alerts.models import ALERT_AuditLog, ALERT_Rule
from src.alerts.services.automation import AutomationEngine
from src.alerts.services.escalation import EscalationEngine
from src.alerts.services.notification import NotificationEngine
from src.transactions.models import ETL_RedFlag


class AlertEngine:
    """Evaluate alert rules and trigger configured actions."""

    def __init__(self, session: Session, company_id: int):
        self.session = session
        self.company_id = company_id
        self.notification_engine = NotificationEngine(session, company_id)
        self.escalation_engine = EscalationEngine(session, company_id)
        self.automation_engine = AutomationEngine(session, company_id)

    def evaluate_rule(self, rule: ALERT_Rule, red_flag: ETL_RedFlag, actor_user_id: int | None = None) -> dict[str, Any]:
        triggered = self._check_conditions(rule.conditions, red_flag)
        if not triggered:
            return {"triggered": False, "actions": []}

        actions_executed: list[dict[str, Any]] = []
        for action in list(rule.actions or []):
            actions_executed.append(self._execute_action(action, red_flag, rule, actor_user_id))

        self.session.add(
            ALERT_AuditLog(
                company_id=self.company_id,
                red_flag_id=red_flag.red_flag_id,
                rule_id=rule.rule_id,
                action="TRIGGERED",
                details={"rule_name": rule.name, "actions": actions_executed},
                performed_by=actor_user_id,
                performed_at=datetime.utcnow(),
            )
        )
        self.session.commit()

        return {"triggered": True, "actions": actions_executed}

    def evaluate_all_rules(self, red_flag: ETL_RedFlag, actor_user_id: int | None = None) -> list[dict[str, Any]]:
        rules = (
            self.session.query(ALERT_Rule)
            .filter(ALERT_Rule.company_id == self.company_id)
            .filter(ALERT_Rule.is_active == True)
            .all()
        )

        results: list[dict[str, Any]] = []
        for rule in rules:
            if rule.category and rule.category.upper() not in {"ALL", "*"}:
                if (red_flag.category or "").upper() != rule.category.upper():
                    continue
            result = self.evaluate_rule(rule, red_flag, actor_user_id=actor_user_id)
            if result["triggered"]:
                results.append({"rule_id": rule.rule_id, "rule_name": rule.name, "actions": result["actions"]})

        return results

    def _check_conditions(self, conditions: dict[str, Any], red_flag: ETL_RedFlag) -> bool:
        if not conditions:
            return False

        # Supports both single-condition and multi-condition payloads.
        clauses = conditions.get("all") or conditions.get("conditions")
        if isinstance(clauses, list):
            op = str(conditions.get("logical_operator", "and")).lower()
            matches = [self._evaluate_condition(clause, red_flag) for clause in clauses if isinstance(clause, dict)]
            if not matches:
                return False
            return any(matches) if op == "or" else all(matches)

        return self._evaluate_condition(conditions, red_flag)

    def _resolve_field_value(self, red_flag: ETL_RedFlag, field: str) -> Any:
        if hasattr(red_flag, field):
            return getattr(red_flag, field)

        if "." in field:
            head, tail = field.split(".", 1)
            nested = getattr(red_flag, head, None)
            if isinstance(nested, dict):
                return nested.get(tail)

        return None

    def _evaluate_condition(self, condition: dict[str, Any], red_flag: ETL_RedFlag) -> bool:
        field = str(condition.get("field") or "").strip()
        operator = str(condition.get("operator") or "eq").lower().strip()
        expected = condition.get("value")

        if not field:
            return False

        value = self._resolve_field_value(red_flag, field)

        if operator == "eq":
            return value == expected
        if operator == "neq":
            return value != expected
        if operator == "gt":
            return value is not None and expected is not None and value > expected
        if operator == "gte":
            return value is not None and expected is not None and value >= expected
        if operator == "lt":
            return value is not None and expected is not None and value < expected
        if operator == "lte":
            return value is not None and expected is not None and value <= expected
        if operator == "in":
            if isinstance(expected, list):
                return value in expected
            return False
        if operator == "like":
            return str(expected or "") in str(value or "")
        if operator == "is_null":
            return value is None
        if operator == "is_not_null":
            return value is not None
        return False

    def _execute_action(
        self,
        action: dict[str, Any],
        red_flag: ETL_RedFlag,
        rule: ALERT_Rule,
        actor_user_id: int | None,
    ) -> dict[str, Any]:
        action_type = str(action.get("type") or "").lower().strip()
        config = action.get("config") or {}

        if action_type == "email":
            subject = str(config.get("subject") or f"Alert: {rule.name}")
            body = str(config.get("body") or self._get_default_email_body(red_flag, rule))
            recipients = list(config.get("recipients") or [])
            result = self.notification_engine.send_email(subject, body, recipients, rule.rule_id, red_flag.red_flag_id)
            return {"type": "email", "result": result}

        if action_type == "webhook":
            payload = {
                "red_flag": {
                    "id": red_flag.red_flag_id,
                    "severity": red_flag.severity,
                    "message": red_flag.message,
                    "created_at": red_flag.created_at.isoformat() if red_flag.created_at else None,
                },
                "rule": {"id": rule.rule_id, "name": rule.name},
            }
            payload.update(config.get("payload") or {})
            result = self.notification_engine.send_webhook(str(config.get("url") or ""), payload, rule.rule_id, red_flag.red_flag_id)
            return {"type": "webhook", "result": result}

        if action_type == "in_app":
            user_ids = [int(v) for v in (config.get("user_ids") or []) if str(v).isdigit()]
            sent_to: list[int] = []
            for user_id in user_ids:
                self.notification_engine.send_in_app(
                    user_id=user_id,
                    subject=str(config.get("subject") or f"Alert: {rule.name}"),
                    message=str(config.get("message") or red_flag.message),
                    payload={"red_flag_id": red_flag.red_flag_id, "rule_id": rule.rule_id},
                    rule_id=rule.rule_id,
                    red_flag_id=red_flag.red_flag_id,
                )
                sent_to.append(user_id)
            return {"type": "in_app", "result": {"success": True, "sent_to": sent_to}}

        if action_type == "auto_resolve":
            if red_flag.severity in {"INFO", "WARNING"} and red_flag.status == "OPEN":
                red_flag.status = "RESOLVED"
                red_flag.resolution_notes = "Auto-resolved by alert rule"
                red_flag.resolved_at = datetime.utcnow()
                red_flag.resolved_by = actor_user_id
                self.session.flush()
                self.session.add(
                    ALERT_AuditLog(
                        company_id=self.company_id,
                        red_flag_id=red_flag.red_flag_id,
                        rule_id=rule.rule_id,
                        action="AUTO_RESOLVED",
                        details={"source": "alert_rule", "rule_name": rule.name},
                        performed_by=actor_user_id,
                        performed_at=datetime.utcnow(),
                    )
                )
                return {"type": "auto_resolve", "result": "resolved"}
            return {"type": "auto_resolve", "result": "skipped"}

        if action_type == "auto_assign":
            assignment = self.automation_engine.auto_assign_to_team(red_flag, priority=int(rule.priority or 1))
            return {"type": "auto_assign", "result": assignment}

        if action_type == "auto_email":
            recipients = list(config.get("recipients") or [])
            subject = str(config.get("subject") or f"Automated Alert: {rule.name}")
            body = self._get_default_email_body(red_flag, rule)
            result = self.notification_engine.send_email(subject, body, recipients, rule.rule_id, red_flag.red_flag_id)
            return {"type": "auto_email", "result": result}

        return {"type": action_type or "unknown", "result": "unknown_action"}

    def _get_default_email_body(self, red_flag: ETL_RedFlag, rule: ALERT_Rule) -> str:
        return f"""
        <h2>Alert: {rule.name}</h2>
        <p><strong>Severity:</strong> {red_flag.severity}</p>
        <p><strong>Category:</strong> {red_flag.category}</p>
        <p><strong>Message:</strong> {red_flag.message}</p>
        <p><strong>Field:</strong> {red_flag.field or '-'}</p>
        <p><strong>Reported:</strong> {red_flag.reported_value or '-'}</p>
        <p><strong>Expected:</strong> {red_flag.expected_value or '-'}</p>
        <p><strong>Created at:</strong> {red_flag.created_at}</p>
        """
