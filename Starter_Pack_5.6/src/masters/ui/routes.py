from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import TRN_TallyExportBatch, TRN_TallyExportDetail

router = APIRouter(prefix="/masters", tags=["UI"])
TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


@router.get("/tally/exports")
async def tally_export_list(
    request: Request,
    export_type: Optional[str] = None,
    export_status: Optional[str] = None,
    sync_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.is_active == True)
    if export_type:
        query = query.filter(TRN_TallyExportBatch.export_type == export_type)
    if export_status:
        query = query.filter(TRN_TallyExportBatch.export_status == export_status)
    if sync_status:
        query = query.filter(TRN_TallyExportBatch.sync_status == sync_status)

    batches = query.order_by(TRN_TallyExportBatch.created_at.desc()).all()
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_list.html",
        {
            "request": request,
            "batches": batches,
            "export_types": ["REVENUE", "COMMISSION", "EXPENSE", "PAYMENT", "ALL"],
            "export_statuses": ["PENDING", "EXPORTING", "COMPLETED", "FAILED"],
            "sync_statuses": ["PENDING", "SYNCED", "FAILED"],
            "selected_export_type": export_type,
            "selected_export_status": export_status,
            "selected_sync_status": sync_status,
        },
    )


@router.get("/tally/exports/add")
async def tally_export_add_form(request: Request):
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_form.html",
        {
            "request": request,
            "batch": None,
            "action": "add",
            "export_types": ["REVENUE", "COMMISSION", "EXPENSE", "PAYMENT", "ALL"],
        },
    )


@router.post("/tally/exports")
async def tally_export_create(
    request: Request,
    batch_name: str = Form(...),
    export_type: str = Form(...),
    period_start: str = Form(...),
    period_end: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    from src.masters.api.tally import create_export_batch, TallyExportBatchCreate

    batch_data = TallyExportBatchCreate(
        batch_name=batch_name,
        export_type=export_type,
        period_start=date.fromisoformat(period_start),
        period_end=date.fromisoformat(period_end),
        notes=notes,
    )
    batch = create_export_batch(batch_data, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch.batch_id}", status_code=303)


@router.get("/tally/exports/{batch_id}")
async def tally_export_detail(request: Request, batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import get_batch_details

    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    details = get_batch_details(batch_id, db)
    return TEMPLATES.TemplateResponse(
        "masters/tally_batch_detail.html",
        {"request": request, "batch": batch, "details": details},
    )


@router.get("/tally/exports/{batch_id}/preview")
async def tally_export_preview(request: Request, batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import get_batch_details

    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    details = get_batch_details(batch_id, db)
    return TEMPLATES.TemplateResponse(
        "masters/tally_export_preview.html",
        {"request": request, "batch": batch, "details": details},
    )


@router.post("/tally/exports/{batch_id}/generate")
async def tally_export_generate(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import generate_export_file

    generate_export_file(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)


@router.post("/tally/exports/{batch_id}/sync")
async def tally_export_sync(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import sync_to_tally

    sync_to_tally(batch_id, db)
    return RedirectResponse(url=f"/masters/tally/exports/{batch_id}", status_code=303)


@router.get("/tally/exports/{batch_id}/delete")
async def tally_export_delete(batch_id: int, db: Session = Depends(get_db)):
    from src.masters.api.tally import delete_export_batch

    delete_export_batch(batch_id, db)
    return RedirectResponse(url="/masters/tally/exports", status_code=303)
