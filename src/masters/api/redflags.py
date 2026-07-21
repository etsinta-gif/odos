from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.security.auth import get_current_user
from src.transactions.models import ETL_ErrorLog

router = APIRouter(
    prefix="/api/admin/redflags",
    tags=["Admin"],
    dependencies=[Depends(get_current_user), Depends(require_company_id)],
)


def _severity(error_type: str) -> str:
    normalized = (error_type or "").upper()
    if normalized in {"VALIDATION", "DUPLICATE"}:
        return "critical"
    if normalized in {"WARNING", "SCHEMA"}:
        return "warning"
    return "info"


@router.get("")
def list_redflags(db: Session = Depends(get_db), limit: int = 200):
    company_id = get_current_company_id()
    limit = max(1, min(limit, 500))

    rows = (
        db.query(ETL_ErrorLog)
        .filter(ETL_ErrorLog.company_id == company_id)
        .order_by(ETL_ErrorLog.error_datetime.desc())
        .limit(limit)
        .all()
    )

    flags = []
    for row in rows:
        severity = _severity(row.error_type)
        flags.append(
            {
                "id": row.error_id,
                "severity": severity,
                "category": row.error_type or "ETL",
                "title": f"{row.table_name} row {row.row_number}",
                "description": row.error_message,
                "source": row.table_name,
                "source_id": row.row_number,
                "created_at": row.error_datetime.isoformat() if row.error_datetime else None,
                "status": "open",
                "actions": [
                    {
                        "label": "View Batch",
                        "action": "open_batch",
                        "batch_guid": row.batch_guid,
                    }
                ],
            }
        )

    return flags
