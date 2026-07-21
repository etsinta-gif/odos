from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.masters.models import MST_Connector, MST_Customer, MST_Lender, MST_Product
from src.security.auth import get_current_user
from src.transactions.models import TRN_Case, TRN_Commission, TRN_Revenue

router = APIRouter(
    prefix="/api/masters/dashboard",
    tags=["Masters"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _company_filter(query, model, company_id: int):
    if hasattr(model, "company_id"):
        query = query.filter(model.company_id == company_id)
    if hasattr(model, "is_active"):
        query = query.filter(model.is_active == True)
    return query


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    company_id = get_current_company_id()

    def count(model):
        return _company_filter(db.query(model), model, company_id).count()

    revenue_total = _company_filter(db.query(func.coalesce(func.sum(TRN_Revenue.net_amount), 0.0)), TRN_Revenue, company_id).scalar() or 0.0
    commission_total = _company_filter(db.query(func.coalesce(func.sum(TRN_Commission.net_amount), 0.0)), TRN_Commission, company_id).scalar() or 0.0

    return {
        "lenders": count(MST_Lender),
        "products": count(MST_Product),
        "customers": count(MST_Customer),
        "cases": count(TRN_Case),
        "connectors": count(MST_Connector),
        "revenue": float(revenue_total),
        "commission": float(commission_total),
    }


@router.get("/activities")
def get_activities(db: Session = Depends(get_db), limit: int = 20):
    company_id = get_current_company_id()
    limit = max(1, min(limit, 100))

    activity_rows: list[dict[str, Any]] = []

    models = [
        (TRN_Case, "case", "Case created/updated"),
        (TRN_Revenue, "revenue", "Revenue entry recorded"),
        (TRN_Commission, "commission", "Commission entry recorded"),
        (MST_Customer, "customer", "Customer profile updated"),
    ]

    for model, item_type, description in models:
        query = _company_filter(db.query(model), model, company_id)
        rows = query.order_by(model.updated_at.desc() if hasattr(model, "updated_at") else model.created_at.desc()).limit(limit).all()
        for row in rows:
            timestamp = getattr(row, "updated_at", None) or getattr(row, "created_at", None)
            item_id = getattr(row, next((c for c in ["case_id", "revenue_id", "commission_id", "customer_id"] if hasattr(row, c)), "id"), 0)
            activity_rows.append(
                {
                    "id": int(item_id or 0),
                    "type": item_type,
                    "action": "updated",
                    "description": description,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                }
            )

    activity_rows.sort(key=lambda r: r.get("timestamp") or "", reverse=True)
    return activity_rows[:limit]
