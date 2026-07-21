from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import TRN_TallyExportBatch, TRN_TallyExportDetail
from src.security.auth import get_current_user
from src.security.models import SEC_User

# Import API functions from the tally API router
from src.masters.api.tally import (
    create_export_batch,
    generate_export_file,
    sync_to_tally,
    delete_export_batch,
    get_export_batch,
    get_batch_details,
    list_export_batches,
)

router = APIRouter(prefix="/masters/tally", tags=["Masters UI"], dependencies=[Depends(get_current_user)])

templates = Jinja2Templates(directory="src/templates")

# Helper lists for filter dropdowns – keep in sync with model enums elsewhere
EXPORT_TYPES = ["REVENUE", "COMMISSION", "EXPENSE", "PAYMENT", "ALL"]
EXPORT_STATUSES = ["PENDING", "EXPORTING", "COMPLETED", "FAILED"]
SYNC_STATUSES = ["PENDING", "SYNCED", "FAILED"]


def _ensure_batch_owner(batch: TRN_TallyExportBatch | None, company_id: int) -> TRN_TallyExportBatch:
    if not batch or getattr(batch, "company_id", None) != company_id:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@router.get("/exports", response_model=None)
def tally_export_list(
    request: Request,
    export_type: str | None = None,
    export_status: str | None = None,
    sync_status: str | None = None,
    current_user: SEC_User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    batches = list_export_batches(
        export_type=export_type,
        export_status=export_status,
        sync_status=sync_status,
        db=db,
    )
    batches = [b for b in batches if getattr(b, "company_id", None) == current_user.company_id]
    return templates.TemplateResponse(
        "masters/tally_batch_list.html",
        {
            "request": request,
            "batches": batches,
            "export_types": EXPORT_TYPES,
            "export_statuses": EXPORT_STATUSES,
            "sync_statuses": SYNC_STATUSES,
            "selected_export_type": export_type,
            "selected_export_status": export_status,
            "selected_sync_status": sync_status,
        },
    )

@router.get("/exports/add")
def tally_export_add_form(request: Request):
    return templates.TemplateResponse(
        "masters/tally_batch_form.html",
        {
            "request": request,
            "batch": None,
            "action": "add",
            "export_types": EXPORT_TYPES,
        },
    )

@router.post("/exports")
def tally_export_create(
    request: Request,
    batch_name: str = Form(...),
    export_type: str = Form(...),
    period_start: str = Form(...),
    period_end: str = Form(...),
    notes: str | None = Form(None),
    current_user: SEC_User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    # Convert date strings to date objects inside the API service
    from src.masters.api.tally import TallyExportBatchCreate
    batch_data = TallyExportBatchCreate(
        batch_name=batch_name,
        export_type=export_type,
        period_start=period_start,  # pydantic will coerce ISO date strings
        period_end=period_end,
        notes=notes,
    )
    batch = create_export_batch(batch_data, db)
    batch.company_id = current_user.company_id
    db.add(batch)
    db.commit()
    return RedirectResponse(url=f"/masters/tally/exports/{batch.batch_id}", status_code=303)

@router.get("/exports/{batch_id}")
def tally_export_detail(
    request: Request,
    batch_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: "Session" = Depends(get_db),
):
    batch = _ensure_batch_owner(get_export_batch(batch_id, db), current_user.company_id)
    details = get_batch_details(batch_id, db)
    return templates.TemplateResponse(
        "masters/tally_batch_detail.html",
        {
            "request": request,
            "batch": batch,
            "details": details,
        },
    )

@router.post("/exports/{batch_id}/generate")
def tally_export_generate(batch_id: int, current_user: SEC_User = Depends(get_current_user), db: "Session" = Depends(get_db)):
    _ensure_batch_owner(get_export_batch(batch_id, db), current_user.company_id)
    generate_export_file(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)

@router.post("/exports/{batch_id}/sync")
def tally_export_sync(batch_id: int, current_user: SEC_User = Depends(get_current_user), db: "Session" = Depends(get_db)):
    _ensure_batch_owner(get_export_batch(batch_id, db), current_user.company_id)
    sync_to_tally(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)

@router.get("/exports/{batch_id}/delete")
def tally_export_delete(batch_id: int, current_user: SEC_User = Depends(get_current_user), db: "Session" = Depends(get_db)):
    _ensure_batch_owner(get_export_batch(batch_id, db), current_user.company_id)
    delete_export_batch(batch_id, db)
    return RedirectResponse(url="/masters/tally/exports", status_code=303)
