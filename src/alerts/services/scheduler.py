from __future__ import annotations

import logging
import os
import threading
import time
from datetime import datetime

from src.alerts.services.alert_engine import AlertEngine
from src.alerts.services.automation import AutomationEngine
from src.alerts.services.escalation import EscalationEngine
from src.core.database import SessionLocal
from src.masters.models import MST_DSA
from src.transactions.models import ETL_RedFlag

logger = logging.getLogger(__name__)


class AlertScheduler:
    """Run periodic alert evaluations, escalations, and automation tasks."""

    def __init__(self) -> None:
        self.running = False
        self.thread: threading.Thread | None = None
        self.interval_rules = int(os.getenv("ALERT_SCHEDULER_RULE_INTERVAL_SEC", "300"))
        self.interval_escalation = int(os.getenv("ALERT_SCHEDULER_ESCALATION_INTERVAL_SEC", "1800"))
        self.interval_auto_resolve = int(os.getenv("ALERT_SCHEDULER_AUTO_RESOLVE_INTERVAL_SEC", "3600"))

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("Alert scheduler started")

    def stop(self) -> None:
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("Alert scheduler stopped")

    def _run(self) -> None:
        last_rules = 0.0
        last_escalation = 0.0
        last_auto_resolve = 0.0

        while self.running:
            now = time.time()
            try:
                if now - last_rules >= self.interval_rules:
                    self.run_rule_checks_once()
                    last_rules = now
                if now - last_escalation >= self.interval_escalation:
                    self.run_escalations_once()
                    last_escalation = now
                if now - last_auto_resolve >= self.interval_auto_resolve:
                    self.run_auto_resolve_once()
                    last_auto_resolve = now
            except Exception as exc:  # pragma: no cover - scheduler is best-effort infra
                logger.error("Alert scheduler tick failed: %s", exc)
            time.sleep(1)

    def _active_companies(self, db) -> list[int]:
        rows = db.query(MST_DSA).filter(MST_DSA.is_active == True).all()
        return [row.dsa_id for row in rows]

    def run_rule_checks_once(self) -> dict:
        db = SessionLocal()
        checked = 0
        triggered = 0
        try:
            for company_id in self._active_companies(db):
                red_flags = (
                    db.query(ETL_RedFlag)
                    .filter(ETL_RedFlag.company_id == company_id)
                    .filter(ETL_RedFlag.status == "OPEN")
                    .all()
                )
                engine = AlertEngine(db, company_id)
                for red_flag in red_flags:
                    checked += 1
                    triggered += len(engine.evaluate_all_rules(red_flag))
            return {"checked_red_flags": checked, "triggered_rules": triggered, "ran_at": datetime.utcnow().isoformat()}
        finally:
            db.close()

    def run_escalations_once(self) -> dict:
        db = SessionLocal()
        escalated = 0
        try:
            for company_id in self._active_companies(db):
                engine = EscalationEngine(db, company_id)
                escalated += len(engine.check_escalations())
            return {"escalated": escalated, "ran_at": datetime.utcnow().isoformat()}
        finally:
            db.close()

    def run_auto_resolve_once(self) -> dict:
        db = SessionLocal()
        total_resolved = 0
        try:
            for company_id in self._active_companies(db):
                engine = AutomationEngine(db, company_id)
                result = engine.auto_resolve_low_severity()
                total_resolved += int(result.get("resolved", 0))
            return {"resolved": total_resolved, "ran_at": datetime.utcnow().isoformat()}
        finally:
            db.close()


scheduler = AlertScheduler()
