from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from src.alerts.models import ALERT_AuditLog
from src.security.models import SEC_User
from src.transactions.models import ETL_RedFlag


class AutomationEngine:
    """Handle automated actions on red flags."""

    def __init__(self, session: Session, company_id: int):
        self.session = session
        self.company_id = company_id

    def auto_resolve_low_severity(self) -> dict:
        resolved: list[int] = []

        rows = (
            self.session.query(ETL_RedFlag)
            .filter(ETL_RedFlag.company_id == self.company_id)
            .filter(ETL_RedFlag.severity == "INFO")
            .filter(ETL_RedFlag.status == "OPEN")
            .all()
        )

        for red_flag in rows:
            red_flag.status = "RESOLVED"
            red_flag.resolution_notes = "Auto-resolved by automation (low severity)"
            red_flag.resolved_at = datetime.utcnow()
            resolved.append(red_flag.red_flag_id)
            self.session.add(
                ALERT_AuditLog(
                    company_id=self.company_id,
                    red_flag_id=red_flag.red_flag_id,
                    action="AUTO_RESOLVED",
                    details={"source": "automation.auto_resolve_low_severity"},
                    performed_at=datetime.utcnow(),
                )
            )

        self.session.commit()
        return {"resolved": len(resolved), "red_flag_ids": resolved}

    def auto_assign_to_team(self, red_flag: ETL_RedFlag, priority: int = 1) -> dict:
        role_by_priority = {
            4: "ADMIN",
            3: "FINANCE",
            2: "OPS",
            1: "OPS",
        }
        role_name = role_by_priority.get(priority, "OPS")

        users = self.session.query(SEC_User).filter(SEC_User.company_id == self.company_id, SEC_User.is_active == True).all()
        assignee = next((u for u in users if u.has_role(role_name)), None)

        if not assignee:
            return {"assigned": False, "message": f"No active user with role {role_name}"}

        self.session.add(
            ALERT_AuditLog(
                company_id=self.company_id,
                red_flag_id=red_flag.red_flag_id,
                action="AUTO_ASSIGNED",
                details={"assigned_to_user_id": assignee.user_id, "assigned_role": role_name},
                performed_at=datetime.utcnow(),
            )
        )
        self.session.commit()

        return {
            "assigned": True,
            "assignee_user_id": assignee.user_id,
            "assignee_username": assignee.username,
            "assignee_role": role_name,
        }
