from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from src.bi.models import BI_ReportDefinition, BI_ReportExecution, BI_ReportSchedule
from src.bi.services.analytics import AnalyticsEngine


class ReportScheduler:
    """Simple DB-driven scheduler for periodic report execution."""

    @staticmethod
    def compute_next_run(config: dict[str, Any], now: datetime | None = None) -> datetime:
        now = now or datetime.utcnow()
        frequency = str(config.get("frequency") or "daily").strip().lower()
        run_time = str(config.get("time") or "09:00").strip()
        hour, minute = 9, 0
        try:
            hour, minute = [int(x) for x in run_time.split(":", 1)]
        except Exception:
            pass

        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if frequency == "daily":
            if candidate <= now:
                candidate = candidate + timedelta(days=1)
            return candidate

        if frequency == "weekly":
            day_name = str(config.get("day") or "monday").strip().lower()
            day_map = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6,
            }
            target = day_map.get(day_name, 0)
            days_ahead = (target - candidate.weekday()) % 7
            if days_ahead == 0 and candidate <= now:
                days_ahead = 7
            return candidate + timedelta(days=days_ahead)

        if frequency == "monthly":
            dom = int(config.get("day") or 1)
            dom = max(1, min(dom, 28))
            month = candidate.month
            year = candidate.year
            month_candidate = candidate.replace(day=dom)
            if month_candidate <= now:
                month = month + 1
                if month > 12:
                    month = 1
                    year += 1
                month_candidate = candidate.replace(year=year, month=month, day=dom)
            return month_candidate

        raise ValueError(f"Unsupported frequency: {frequency}")

    @classmethod
    def upsert_schedule(
        cls,
        db: Session,
        report: BI_ReportDefinition,
        schedule_config: dict[str, Any],
        user_id: int | None,
    ) -> BI_ReportSchedule:
        schedule = (
            db.query(BI_ReportSchedule)
            .filter(BI_ReportSchedule.report_id == report.report_id)
            .filter(BI_ReportSchedule.company_id == report.company_id)
            .filter(BI_ReportSchedule.is_active == True)
            .first()
        )

        frequency = str(schedule_config.get("frequency") or "daily").strip().upper()
        day_val = schedule_config.get("day")
        recipients = schedule_config.get("recipients") if isinstance(schedule_config.get("recipients"), list) else []

        next_run = cls.compute_next_run(schedule_config)

        if schedule is None:
            schedule = BI_ReportSchedule(
                report_id=report.report_id,
                company_id=report.company_id,
                frequency=frequency,
                day_of_week=str(day_val).upper() if frequency == "WEEKLY" and day_val else None,
                day_of_month=int(day_val) if frequency == "MONTHLY" and day_val is not None else None,
                run_time=str(schedule_config.get("time") or "09:00"),
                recipients=recipients,
                next_run_at=next_run,
                is_active=True,
                created_by=user_id,
                updated_by=user_id,
            )
            db.add(schedule)
        else:
            schedule.frequency = frequency
            schedule.day_of_week = str(day_val).upper() if frequency == "WEEKLY" and day_val else None
            schedule.day_of_month = int(day_val) if frequency == "MONTHLY" and day_val is not None else None
            schedule.run_time = str(schedule_config.get("time") or "09:00")
            schedule.recipients = recipients
            schedule.next_run_at = next_run
            schedule.updated_by = user_id

        report.is_scheduled = True
        report.schedule_config = schedule_config
        report.updated_by = user_id
        return schedule

    @staticmethod
    def run_due_reports(db: Session, company_id: int | None = None) -> dict[str, Any]:
        now = datetime.utcnow()
        query = db.query(BI_ReportSchedule).filter(BI_ReportSchedule.is_active == True)
        query = query.filter(BI_ReportSchedule.next_run_at.is_not(None)).filter(BI_ReportSchedule.next_run_at <= now)
        if company_id is not None:
            query = query.filter(BI_ReportSchedule.company_id == company_id)

        schedules = query.all()
        executed = 0
        failed = 0

        for schedule in schedules:
            report = (
                db.query(BI_ReportDefinition)
                .filter(BI_ReportDefinition.report_id == schedule.report_id)
                .filter(BI_ReportDefinition.company_id == schedule.company_id)
                .filter(BI_ReportDefinition.is_active == True)
                .first()
            )
            if report is None:
                continue

            execution = BI_ReportExecution(
                report_id=report.report_id,
                company_id=report.company_id,
                triggered_by=schedule.updated_by,
                status="PROCESSING",
            )
            db.add(execution)
            db.flush()

            try:
                engine = AnalyticsEngine(db, report.company_id)
                result = engine.execute_report(report.report_id, definition=dict(report.definition or {}))
                execution.status = "COMPLETED"
                execution.completed_at = now
                execution.row_count = result.get("row_count", 0)
                schedule.last_run_at = now
                schedule.next_run_at = ReportScheduler.compute_next_run(report.schedule_config or {})
                executed += 1
            except Exception as exc:
                execution.status = "FAILED"
                execution.error_message = str(exc)
                failed += 1

        db.commit()
        return {"processed": len(schedules), "executed": executed, "failed": failed}
