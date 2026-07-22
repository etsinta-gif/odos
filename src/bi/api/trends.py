from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.bi.services.analytics import AnalyticsEngine
from src.core.database import get_db
from src.core.tenant import require_company_id
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(
    prefix="/api/bi/trends",
    tags=["BI"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _require_read_role(user: SEC_User) -> None:
    roles = {role.role_name.upper() for role in user.roles}
    if not (roles & {"ADMIN", "FINANCE", "AUDITOR"}):
        raise HTTPException(status_code=403, detail="Insufficient permissions")


@router.get("/summary")
def trend_summary(
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_read_role(current_user)
    engine = AnalyticsEngine(db, current_user.company_id)
    return {
        "gst_mismatches": engine.get_trend_data("gst_mismatch", 7),
        "tds_mismatches": engine.get_trend_data("tds_mismatch", 7),
        "commission_exceeds": engine.get_trend_data("commission_exceed", 7),
        "red_flags": engine.get_trend_data("red_flag_count", 7),
    }


@router.get("/{metric_type}")
def trend_by_metric(
    metric_type: str,
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: SEC_User = Depends(get_current_user),
):
    _require_read_role(current_user)
    try:
        engine = AnalyticsEngine(db, current_user.company_id)
        return engine.get_trend_data(metric_type, days)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
