from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.alerts.models import ALERT_AuditLog, ALERT_EscalationPolicy
from src.security.models import SEC_User
from src.transactions.models import ETL_RedFlag


SEVERITY_ORDER = ["INFO", "WARNING", "CRITICAL"]


class EscalationEngine:
    """Handle escalation workflows and SLA metrics."""

    def __init__(self, session: Session, company_id: int):
        self.session = session
        self.company_id = company_id

    def check_escalations(self) -> list[dict]:
        escalated: list[dict] = []

        red_flags = (
            self.session.query(ETL_RedFlag)
            .filter(ETL_RedFlag.company_id == self.company_id)
            .filter(ETL_RedFlag.status == "OPEN")
            .all()
        )

        policies = (
            self.session.query(ALERT_EscalationPolicy)
            .filter(ALERT_EscalationPolicy.company_id == self.company_id)
            .filter(ALERT_EscalationPolicy.is_active == True)
            .all()
        )
        default_policy = policies[0] if policies else None

        for red_flag in red_flags:
            elapsed_minutes = (datetime.utcnow() - red_flag.created_at).total_seconds() / 60.0
            threshold = 24 * 60
            next_role = None

            if default_policy and default_policy.levels:
                levels = sorted(default_policy.levels, key=lambda x: int(x.get("level", 0)))
                escalation_count = (
                    self.session.query(ALERT_AuditLog)
                    .filter(ALERT_AuditLog.company_id == self.company_id)
                    .filter(ALERT_AuditLog.red_flag_id == red_flag.red_flag_id)
                    .filter(ALERT_AuditLog.action == "ESCALATED")
                    .count()
                )
                next_level = levels[min(escalation_count, len(levels) - 1)]
                threshold = int(next_level.get("time_minutes", threshold))
                next_role = next_level.get("assign_to_role")

            if elapsed_minutes < threshold:
                continue

            result = self._escalate(red_flag, elapsed_minutes, threshold, next_role)
            escalated.append({"red_flag_id": red_flag.red_flag_id, "escalation": result})

        if escalated:
            self.session.commit()
        return escalated

    def _escalate(self, red_flag: ETL_RedFlag, elapsed_minutes: float, threshold: int, next_role: str | None) -> dict:
        from_severity = red_flag.severity
        try:
            idx = SEVERITY_ORDER.index((red_flag.severity or "INFO").upper())
        except ValueError:
            idx = 0
        to_severity = SEVERITY_ORDER[min(idx + 1, len(SEVERITY_ORDER) - 1)]
        red_flag.severity = to_severity

        details = {
            "from_severity": from_severity,
            "to_severity": to_severity,
            "elapsed_minutes": round(elapsed_minutes, 2),
            "threshold_minutes": threshold,
            "escalated_at": datetime.utcnow().isoformat(),
        }

        if next_role:
            notified = self._notify_role(next_role, red_flag)
            details["notified_role"] = next_role
            details["notified_users"] = notified

        self.session.add(
            ALERT_AuditLog(
                company_id=self.company_id,
                red_flag_id=red_flag.red_flag_id,
                action="ESCALATED",
                details=details,
                performed_at=datetime.utcnow(),
            )
        )

        return details

    def _notify_role(self, role_name: str, red_flag: ETL_RedFlag) -> list[int]:
        users = self.session.query(SEC_User).filter(SEC_User.company_id == self.company_id, SEC_User.is_active == True).all()
        recipients = [u for u in users if u.has_role(role_name)]

        notified_ids: list[int] = []
        from src.alerts.services.notification import NotificationEngine

        notifier = NotificationEngine(self.session, self.company_id)
        for user in recipients:
            notifier.send_in_app(
                user_id=user.user_id,
                subject=f"Escalated Red Flag #{red_flag.red_flag_id}",
                message=f"Red flag {red_flag.red_flag_id} escalated to {red_flag.severity}",
                payload={"red_flag_id": red_flag.red_flag_id, "severity": red_flag.severity},
                red_flag_id=red_flag.red_flag_id,
            )
            notified_ids.append(user.user_id)
        return notified_ids

    def calculate_sla_metrics(self, red_flag: ETL_RedFlag, sla_minutes: int = 24 * 60) -> dict:
        now = datetime.utcnow()
        response_time = (now - red_flag.created_at).total_seconds() / 60.0
        resolution_time = None
        if red_flag.status == "RESOLVED" and red_flag.resolved_at:
            resolution_time = (red_flag.resolved_at - red_flag.created_at).total_seconds() / 60.0

        return {
            "response_time": round(response_time, 2),
            "resolution_time": round(resolution_time, 2) if resolution_time is not None else None,
            "breached": response_time > sla_minutes,
            "sla_minutes": sla_minutes,
        }
