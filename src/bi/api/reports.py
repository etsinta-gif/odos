from __future__ import annotations

from datetime import datetime
from time import perf_counter
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.bi.models import BI_ReportDefinition, BI_ReportExecution, BI_ReportSchedule
from src.bi.services.analytics import AnalyticsEngine
from src.bi.services.report_generator import ReportGenerator
from src.bi.services.scheduler import ReportScheduler
from src.core.database import get_db
from src.core.tenant import require_company_id
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(
    prefix="/api/bi/reports",
    tags=["BI"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _role_names(user: SEC_User) -> set[str]:
    return {role.role_name.upper() for role in user.roles}


def _require_any_role(user: SEC_User, allowed: set[str]) -> None:
    if not (_role_names(user) & allowed):
        raise HTTPException(status_code=403, detail="Insufficient permissions")


class ReportDefinitionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str = "Custom"
    definition: dict[str, Any]
    output_format: str = "HTML"
    is_scheduled: bool = False
    schedule_config: Optional[dict[str, Any]] = None
    is_public: bool = False


class ReportDefinitionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    definition: Optional[dict[str, Any]] = None
    output_format: Optional[str] = None
    is_scheduled: Optional[bool] = None
    schedule_config: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None


class ReportDefinitionResponse(BaseModel):
    report_id: int
    name: str
    description: Optional[str]
    category: str
    output_format: str
    is_scheduled: bool
    is_active: bool
    is_public: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ScheduleUpsertRequest(BaseModel):
    frequency: str
    day: Optional[str] = None
    time: str = "09:00"
    recipients: list[str] = []


@router.get("/", response_model=list[ReportDefinitionResponse])
def list_reports(
    category: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN", "FINANCE", "AUDITOR"})

    query = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .filter(BI_ReportDefinition.is_active == True)
    )
    if category:
        query = query.filter(BI_ReportDefinition.category == category)

    query = query.filter((BI_ReportDefinition.is_public == True) | (BI_ReportDefinition.created_by == current_user.user_id))
    return query.order_by(BI_ReportDefinition.report_id.desc()).all()


@router.get("/{report_id}", response_model=ReportDefinitionResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN", "FINANCE", "AUDITOR"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if not report.is_public and report.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return report


@router.post("/", response_model=ReportDefinitionResponse)
def create_report(
    report_data: ReportDefinitionCreate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})

    report = BI_ReportDefinition(
        company_id=current_user.company_id,
        name=report_data.name,
        description=report_data.description,
        category=report_data.category,
        definition=report_data.definition,
        output_format=report_data.output_format.upper(),
        is_scheduled=bool(report_data.is_scheduled),
        schedule_config=report_data.schedule_config,
        is_public=bool(report_data.is_public),
        is_active=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
    )
    db.add(report)
    db.flush()

    if report.is_scheduled and report.schedule_config:
        ReportScheduler.upsert_schedule(db, report, report.schedule_config, current_user.user_id)

    db.commit()
    db.refresh(report)
    return report


@router.put("/{report_id}")
def update_report(
    report_id: int,
    report_data: ReportDefinitionUpdate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, value in report_data.model_dump(exclude_unset=True).items():
        if field == "output_format" and isinstance(value, str):
            setattr(report, field, value.upper())
        else:
            setattr(report, field, value)

    report.updated_by = current_user.user_id

    if report.is_scheduled and report.schedule_config:
        ReportScheduler.upsert_schedule(db, report, report.schedule_config, current_user.user_id)

    db.commit()
    db.refresh(report)
    return report


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    if report.created_by != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    report.is_active = False
    report.updated_by = current_user.user_id
    db.commit()
    return {"message": "Report deleted"}


@router.post("/{report_id}/execute")
def execute_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN", "FINANCE"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .filter(BI_ReportDefinition.is_active == True)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    execution = BI_ReportExecution(
        report_id=report.report_id,
        company_id=current_user.company_id,
        triggered_by=current_user.user_id,
        status="PROCESSING",
    )
    db.add(execution)
    db.flush()

    started = perf_counter()
    try:
        engine = AnalyticsEngine(db, current_user.company_id)
        result = engine.execute_report(report.report_id, definition=dict(report.definition or {}))
        elapsed_ms = int((perf_counter() - started) * 1000)
        execution.status = "COMPLETED"
        execution.completed_at = datetime.utcnow()
        execution.row_count = result.get("row_count")
        execution.execution_time_ms = elapsed_ms
        db.commit()
        return result
    except Exception as exc:
        execution.status = "FAILED"
        execution.error_message = str(exc)
        db.commit()
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{report_id}/export/{fmt}")
def export_report(
    report_id: int,
    fmt: str,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN", "FINANCE", "AUDITOR"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .filter(BI_ReportDefinition.is_active == True)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    engine = AnalyticsEngine(db, current_user.company_id)
    result = engine.execute_report(report.report_id, definition=dict(report.definition or {}))

    company_name = getattr(current_user, "company_name", None) or f"Company {current_user.company_id}"
    generator = ReportGenerator(result, report.name, company_name)

    format_name = fmt.lower().strip()
    if format_name == "pdf":
        content = generator.to_pdf()
        media_type = "application/pdf"
        ext = "pdf"
    elif format_name in {"excel", "xlsx"}:
        content = generator.to_excel()
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ext = "xlsx"
    elif format_name == "csv":
        content = generator.to_csv().encode("utf-8")
        media_type = "text/csv"
        ext = "csv"
    else:
        content = generator.to_html().encode("utf-8")
        media_type = "text/html"
        ext = "html"

    safe_name = "_".join(report.name.strip().split()) or "report"
    filename = f"{safe_name}_{datetime.utcnow().strftime('%Y%m%d')}.{ext}"
    return Response(content=content, media_type=media_type, headers={"Content-Disposition": f"attachment; filename={filename}"})


@router.post("/{report_id}/schedule")
def upsert_schedule(
    report_id: int,
    payload: ScheduleUpsertRequest,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})

    report = (
        db.query(BI_ReportDefinition)
        .filter(BI_ReportDefinition.report_id == report_id)
        .filter(BI_ReportDefinition.company_id == current_user.company_id)
        .filter(BI_ReportDefinition.is_active == True)
        .first()
    )
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    config = payload.model_dump()
    schedule = ReportScheduler.upsert_schedule(db, report, config, current_user.user_id)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.get("/{report_id}/schedules")
def list_schedules(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN", "FINANCE", "AUDITOR"})

    return (
        db.query(BI_ReportSchedule)
        .filter(BI_ReportSchedule.report_id == report_id)
        .filter(BI_ReportSchedule.company_id == current_user.company_id)
        .filter(BI_ReportSchedule.is_active == True)
        .all()
    )


@router.post("/scheduler/run")
def run_scheduler(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_any_role(current_user, {"ADMIN"})
    return ReportScheduler.run_due_reports(db, company_id=current_user.company_id)
