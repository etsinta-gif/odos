from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.bi.models import BI_DashboardDefinition, BI_WidgetDefinition
from src.bi.services.analytics import AnalyticsEngine
from src.core.database import get_db
from src.core.tenant import require_company_id
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(
    prefix="/api/bi/dashboards",
    tags=["BI"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _require_write_role(user: SEC_User) -> None:
    roles = {role.role_name.upper() for role in user.roles}
    if not (roles & {"ADMIN", "FINANCE"}):
        raise HTTPException(status_code=403, detail="Insufficient permissions")


def _require_read_role(user: SEC_User) -> None:
    roles = {role.role_name.upper() for role in user.roles}
    if not (roles & {"ADMIN", "FINANCE", "AUDITOR"}):
        raise HTTPException(status_code=403, detail="Insufficient permissions")


class DashboardCreate(BaseModel):
    name: str
    description: Optional[str] = None
    layout: dict[str, Any] = {}
    is_default: bool = False


class DashboardUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    layout: Optional[dict[str, Any]] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class WidgetCreate(BaseModel):
    title: str
    type: str
    chart_type: Optional[str] = None
    report_id: Optional[int] = None
    query_definition: Optional[dict[str, Any]] = None
    position_x: int = 0
    position_y: int = 0
    width: int = 4
    height: int = 3


@router.get("/")
def list_dashboards(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_read_role(current_user)
    return (
        db.query(BI_DashboardDefinition)
        .filter(BI_DashboardDefinition.company_id == current_user.company_id)
        .filter(BI_DashboardDefinition.is_active == True)
        .order_by(BI_DashboardDefinition.dashboard_id.desc())
        .all()
    )


@router.post("/")
def create_dashboard(
    payload: DashboardCreate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_write_role(current_user)
    dashboard = BI_DashboardDefinition(
        company_id=current_user.company_id,
        name=payload.name,
        description=payload.description,
        layout=payload.layout,
        is_default=payload.is_default,
        is_active=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
    )
    db.add(dashboard)
    db.commit()
    db.refresh(dashboard)
    return dashboard


@router.get("/{dashboard_id}")
def get_dashboard(
    dashboard_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_read_role(current_user)

    dashboard = (
        db.query(BI_DashboardDefinition)
        .filter(BI_DashboardDefinition.dashboard_id == dashboard_id)
        .filter(BI_DashboardDefinition.company_id == current_user.company_id)
        .filter(BI_DashboardDefinition.is_active == True)
        .first()
    )
    if dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    widgets = (
        db.query(BI_WidgetDefinition)
        .filter(BI_WidgetDefinition.dashboard_id == dashboard_id)
        .filter(BI_WidgetDefinition.company_id == current_user.company_id)
        .filter(BI_WidgetDefinition.is_active == True)
        .order_by(BI_WidgetDefinition.widget_id.asc())
        .all()
    )

    return {
        "dashboard_id": dashboard.dashboard_id,
        "name": dashboard.name,
        "description": dashboard.description,
        "layout": dashboard.layout,
        "is_default": dashboard.is_default,
        "widgets": widgets,
    }


@router.put("/{dashboard_id}")
def update_dashboard(
    dashboard_id: int,
    payload: DashboardUpdate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_write_role(current_user)
    dashboard = (
        db.query(BI_DashboardDefinition)
        .filter(BI_DashboardDefinition.dashboard_id == dashboard_id)
        .filter(BI_DashboardDefinition.company_id == current_user.company_id)
        .first()
    )
    if dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(dashboard, field, value)

    dashboard.updated_by = current_user.user_id
    dashboard.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(dashboard)
    return dashboard


@router.delete("/{dashboard_id}")
def delete_dashboard(
    dashboard_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_write_role(current_user)

    dashboard = (
        db.query(BI_DashboardDefinition)
        .filter(BI_DashboardDefinition.dashboard_id == dashboard_id)
        .filter(BI_DashboardDefinition.company_id == current_user.company_id)
        .first()
    )
    if dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    dashboard.is_active = False
    dashboard.updated_by = current_user.user_id

    widgets = db.query(BI_WidgetDefinition).filter(BI_WidgetDefinition.dashboard_id == dashboard_id).all()
    for widget in widgets:
        widget.is_active = False

    db.commit()
    return {"message": "Dashboard deleted"}


@router.post("/{dashboard_id}/widgets")
def add_widget(
    dashboard_id: int,
    payload: WidgetCreate,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_write_role(current_user)

    dashboard = (
        db.query(BI_DashboardDefinition)
        .filter(BI_DashboardDefinition.dashboard_id == dashboard_id)
        .filter(BI_DashboardDefinition.company_id == current_user.company_id)
        .filter(BI_DashboardDefinition.is_active == True)
        .first()
    )
    if dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")

    widget = BI_WidgetDefinition(
        dashboard_id=dashboard_id,
        company_id=current_user.company_id,
        title=payload.title,
        type=payload.type.upper(),
        chart_type=payload.chart_type.upper() if payload.chart_type else None,
        report_id=payload.report_id,
        query_definition=payload.query_definition,
        position_x=max(0, payload.position_x),
        position_y=max(0, payload.position_y),
        width=max(1, min(12, payload.width)),
        height=max(1, min(12, payload.height)),
        is_active=True,
        created_by=current_user.user_id,
        updated_by=current_user.user_id,
    )
    db.add(widget)
    db.commit()
    db.refresh(widget)
    return widget


@router.post("/{dashboard_id}/widgets/{widget_id}/execute")
def execute_widget(
    dashboard_id: int,
    widget_id: int,
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_read_role(current_user)

    widget = (
        db.query(BI_WidgetDefinition)
        .filter(BI_WidgetDefinition.widget_id == widget_id)
        .filter(BI_WidgetDefinition.dashboard_id == dashboard_id)
        .filter(BI_WidgetDefinition.company_id == current_user.company_id)
        .filter(BI_WidgetDefinition.is_active == True)
        .first()
    )
    if widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")

    if widget.query_definition:
        engine = AnalyticsEngine(db, current_user.company_id)
        return engine.execute_definition(dict(widget.query_definition))

    if widget.report_id:
        engine = AnalyticsEngine(db, current_user.company_id)
        return engine.execute_report(widget.report_id)

    raise HTTPException(status_code=400, detail="Widget has neither report_id nor query_definition")
