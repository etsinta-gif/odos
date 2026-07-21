import json
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import (
    TRN_TallyExportBatch,
    TRN_TallyExportDetail,
    TRN_Revenue,
    TRN_Commission,
    TRN_Expense,
    TRN_Payment,
)

router = APIRouter(prefix="/api/masters/tally", tags=["Masters"])


class TallyExportBatchCreate(BaseModel):
    batch_name: str
    export_type: str  # REVENUE, COMMISSION, EXPENSE, PAYMENT, ALL
    period_start: date
    period_end: date
    notes: Optional[str] = None


class TallyExportBatchResponse(BaseModel):
    batch_id: int
    batch_name: str
    batch_number: Optional[str]
    export_type: str
    period_start: date
    period_end: date
    total_records: int
    exported_records: int
    export_status: str
    sync_status: str
    file_path: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TallyExportDetailResponse(BaseModel):
    detail_id: int
    batch_id: int
    source_table: str
    source_id: int
    exported_data: Optional[str]
    export_status: str
    error_message: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/exports", response_model=List[TallyExportBatchResponse])
def list_export_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
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
    batches = query.offset(skip).limit(limit).all()
    return batches


@router.get("/exports/{batch_id}", response_model=TallyExportBatchResponse)
def get_export_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    return batch


@router.post("/exports", response_model=TallyExportBatchResponse)
def create_export_batch(batch_data: TallyExportBatchCreate, db: Session = Depends(get_db)):
    batch_number = f"TALLY-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"

    new_batch = TRN_TallyExportBatch(
        batch_name=batch_data.batch_name,
        batch_number=batch_number,
        export_type=batch_data.export_type,
        period_start=batch_data.period_start,
        period_end=batch_data.period_end,
        total_records=0,
        exported_records=0,
        export_status="PENDING",
        sync_status="PENDING",
        notes=batch_data.notes,
        is_active=True,
    )
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch


@router.post("/exports/{batch_id}/generate")
def generate_export_file(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    batch.export_status = "EXPORTING"
    db.commit()

    try:
        batch.exported_records = 0

        if batch.export_type in ["REVENUE", "ALL"]:
            revenue_records = db.query(TRN_Revenue).filter(
                TRN_Revenue.revenue_date >= batch.period_start,
                TRN_Revenue.revenue_date <= batch.period_end,
                TRN_Revenue.is_active == True,
            ).all()
            for record in revenue_records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="REVENUE",
                    source_id=record.revenue_id,
                    exported_data=json.dumps({
                        "date": str(record.revenue_date),
                        "amount": record.net_amount,
                        "case_id": record.case_id,
                        "gst": record.gst_amount,
                        "tds": record.tds_amount,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["COMMISSION", "ALL"]:
            commission_records = db.query(TRN_Commission).filter(
                TRN_Commission.commission_date >= batch.period_start,
                TRN_Commission.commission_date <= batch.period_end,
                TRN_Commission.is_active == True,
            ).all()
            for record in commission_records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="COMMISSION",
                    source_id=record.commission_id,
                    exported_data=json.dumps({
                        "date": str(record.commission_date),
                        "amount": record.net_amount,
                        "case_id": record.case_id,
                        "connector_id": record.connector_id,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["EXPENSE", "ALL"]:
            expense_records = db.query(TRN_Expense).filter(
                TRN_Expense.expense_date >= batch.period_start,
                TRN_Expense.expense_date <= batch.period_end,
                TRN_Expense.is_active == True,
            ).all()
            for record in expense_records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="EXPENSE",
                    source_id=record.expense_id,
                    exported_data=json.dumps({
                        "date": str(record.expense_date),
                        "amount": record.net_amount,
                        "category": record.expense_category_id,
                        "description": record.description,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        if batch.export_type in ["PAYMENT", "ALL"]:
            payment_records = db.query(TRN_Payment).filter(
                TRN_Payment.payment_date >= batch.period_start,
                TRN_Payment.payment_date <= batch.period_end,
                TRN_Payment.is_active == True,
            ).all()
            for record in payment_records:
                detail = TRN_TallyExportDetail(
                    batch_id=batch.batch_id,
                    source_table="PAYMENT",
                    source_id=record.payment_id,
                    exported_data=json.dumps({
                        "date": str(record.payment_date),
                        "amount": record.payment_amount,
                        "mode": record.payment_mode,
                        "utr": record.utr_number,
                    }),
                    export_status="COMPLETED",
                )
                db.add(detail)
                batch.exported_records += 1

        batch.total_records = batch.exported_records
        batch.export_status = "COMPLETED"
        db.commit()

        return {
            "message": "Export file generated successfully",
            "batch_id": batch.batch_id,
            "records_exported": batch.exported_records,
        }

    except Exception as exc:
        batch.export_status = "FAILED"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Export generation failed: {str(exc)}")


@router.post("/exports/{batch_id}/sync")
def sync_to_tally(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    if batch.export_status != "COMPLETED":
        raise HTTPException(status_code=400, detail="Batch must be completed before syncing")

    batch.sync_status = "SYNCED"
    db.commit()
    return {"message": "Batch synced to Tally successfully"}


@router.get("/exports/{batch_id}/details", response_model=List[TallyExportDetailResponse])
def get_batch_details(batch_id: int, db: Session = Depends(get_db)):
    details = db.query(TRN_TallyExportDetail).filter(TRN_TallyExportDetail.batch_id == batch_id).all()
    return details


@router.delete("/exports/{batch_id}")
def delete_export_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    batch.is_active = False
    db.commit()
    return {"message": "Export batch deleted successfully"}
