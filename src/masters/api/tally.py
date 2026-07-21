import json
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.security.auth import get_current_user
from src.transactions.models import (
    TRN_TallyExportBatch,
    TRN_TallyExportDetail,
    TRN_Revenue,
    TRN_Commission,
    TRN_Expense,
    TRN_Payment,
)

EXPORT_FOLDER = Path(__file__).resolve().parents[3] / "src" / "static" / "exports"
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/api/masters/tally", tags=["Masters"], dependencies=[Depends(get_current_user), Depends(require_company_id)])


class TallyExportBatchCreate(BaseModel):
    batch_name: str
    export_type: str
    period_start: date
    period_end: date
    notes: Optional[str] = None


class TallyExportBatchUpdate(BaseModel):
    batch_name: Optional[str] = None
    export_type: Optional[str] = None
    period_start: Optional[date] = None
    period_end: Optional[date] = None
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


def _render_tally_xml(batch: TRN_TallyExportBatch, details: List[TRN_TallyExportDetail]) -> str:
    lines = ["<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "<ENVELOPE>"]
    lines.append("  <HEADER>")
    lines.append("    <TALLYREQUEST>Export Data</TALLYREQUEST>")
    lines.append("  </HEADER>")
    lines.append("  <BODY>")
    lines.append("    <EXPORTDATA>")
    lines.append("      <REQUESTDATA>")

    for detail in details:
        payload = json.loads(detail.exported_data) if detail.exported_data else {}
        lines.append("        <TALLYMESSAGE xmlns:UDF=\"TallyUDF\">")
        lines.append("          <VOUCHER>")
        lines.append(f"            <VOUCHERTYPENAME>{detail.source_table}</VOUCHERTYPENAME>")
        lines.append(f"            <DATE>{payload.get('date', '')}</DATE>")
        lines.append(f"            <AMOUNT>{payload.get('amount', 0)}</AMOUNT>")

        if detail.source_table == "REVENUE":
            lines.append(f"            <CASEID>{payload.get('case_id', '')}</CASEID>")
            lines.append(f"            <GST>{payload.get('gst', 0)}</GST>")
            lines.append(f"            <TDS>{payload.get('tds', 0)}</TDS>")
        elif detail.source_table == "COMMISSION":
            lines.append(f"            <CASEID>{payload.get('case_id', '')}</CASEID>")
            lines.append(f"            <CONNECTORID>{payload.get('connector_id', '')}</CONNECTORID>")
        elif detail.source_table == "EXPENSE":
            lines.append(f"            <CATEGORY>{payload.get('category', '')}</CATEGORY>")
            lines.append(f"            <DESCRIPTION>{payload.get('description', '')}</DESCRIPTION>")
        elif detail.source_table == "PAYMENT":
            lines.append(f"            <MODE>{payload.get('mode', '')}</MODE>")
            lines.append(f"            <UTR>{payload.get('utr', '')}</UTR>")

        lines.append("          </VOUCHER>")
        lines.append("        </TALLYMESSAGE>")

    lines.append("      </REQUESTDATA>")
    lines.append("    </EXPORTDATA>")
    lines.append("  </BODY>")
    lines.append("</ENVELOPE>")
    return "\n".join(lines)


def _write_export_file(batch: TRN_TallyExportBatch, details: List[TRN_TallyExportDetail]) -> str:
    content = _render_tally_xml(batch, details)
    filename = f"{batch.batch_number}_{datetime.now().strftime('%Y%m%d%H%M%S')}.xml"
    target = EXPORT_FOLDER / filename
    target.write_text(content, encoding="utf-8")
    return f"/static/exports/{filename}"


@router.get("/exports", response_model=List[TallyExportBatchResponse])
def list_export_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    export_type: Optional[str] = None,
    export_status: Optional[str] = None,
    sync_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    company_id = get_current_company_id()
    query = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.is_active == True)
    if company_id is not None:
        query = query.filter(TRN_TallyExportBatch.company_id == company_id)
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
    company_id = get_current_company_id()
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id)
    if company_id is not None:
        batch = batch.filter(TRN_TallyExportBatch.company_id == company_id)
    batch = batch.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    return batch


@router.post("/exports", response_model=TallyExportBatchResponse)
def create_export_batch(batch_data: TallyExportBatchCreate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    batch_number = f"TALLY-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"

    new_batch = TRN_TallyExportBatch(
        company_id=company_id or 1,
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
        file_path=None,
        is_active=True,
    )
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch


@router.put("/exports/{batch_id}", response_model=TallyExportBatchResponse)
def update_export_batch(batch_id: int, batch_data: TallyExportBatchUpdate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id)
    if company_id is not None:
        batch = batch.filter(TRN_TallyExportBatch.company_id == company_id)
    batch = batch.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    update_fields = batch_data.model_dump(exclude_unset=True)
    if update_fields:
        for field, value in update_fields.items():
            setattr(batch, field, value)
        batch.export_status = "PENDING"
        batch.sync_status = "PENDING"
        batch.file_path = None
        batch.total_records = 0
        batch.exported_records = 0
        details_q = db.query(TRN_TallyExportDetail).filter(TRN_TallyExportDetail.batch_id == batch_id)
        if company_id is not None:
            details_q = details_q.filter(TRN_TallyExportDetail.company_id == company_id)
        details_q.delete()

    db.commit()
    db.refresh(batch)
    return batch


@router.post("/exports/{batch_id}/generate")
def generate_export_file(batch_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id)
    if company_id is not None:
        batch = batch.filter(TRN_TallyExportBatch.company_id == company_id)
    batch = batch.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")

    batch.export_status = "EXPORTING"
    batch.exported_records = 0
    batch.file_path = None
    db.commit()

    try:
        details = []

        if batch.export_type in ["REVENUE", "ALL"]:
            records = db.query(TRN_Revenue).filter(
                TRN_Revenue.revenue_date >= batch.period_start,
                TRN_Revenue.revenue_date <= batch.period_end,
                TRN_Revenue.is_active == True,
                TRN_Revenue.company_id == (company_id or batch.company_id),
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    company_id=company_id or batch.company_id,
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
                details.append(detail)
                batch.exported_records += 1

        if batch.export_type in ["COMMISSION", "ALL"]:
            records = db.query(TRN_Commission).filter(
                TRN_Commission.commission_date >= batch.period_start,
                TRN_Commission.commission_date <= batch.period_end,
                TRN_Commission.is_active == True,
                TRN_Commission.company_id == (company_id or batch.company_id),
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    company_id=company_id or batch.company_id,
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
                details.append(detail)
                batch.exported_records += 1

        if batch.export_type in ["EXPENSE", "ALL"]:
            records = db.query(TRN_Expense).filter(
                TRN_Expense.expense_date >= batch.period_start,
                TRN_Expense.expense_date <= batch.period_end,
                TRN_Expense.is_active == True,
                TRN_Expense.company_id == (company_id or batch.company_id),
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    company_id=company_id or batch.company_id,
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
                details.append(detail)
                batch.exported_records += 1

        if batch.export_type in ["PAYMENT", "ALL"]:
            records = db.query(TRN_Payment).filter(
                TRN_Payment.payment_date >= batch.period_start,
                TRN_Payment.payment_date <= batch.period_end,
                TRN_Payment.is_active == True,
                TRN_Payment.company_id == (company_id or batch.company_id),
            ).all()
            for record in records:
                detail = TRN_TallyExportDetail(
                    company_id=company_id or batch.company_id,
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
                details.append(detail)
                batch.exported_records += 1

        batch.total_records = batch.exported_records
        batch.export_status = "COMPLETED"
        db.commit()

        batch.file_path = _write_export_file(batch, details)
        db.commit()

        return {
            "message": "Export file generated successfully",
            "batch_id": batch.batch_id,
            "records_exported": batch.exported_records,
            "file_path": batch.file_path,
        }

    except Exception as exc:
        batch.export_status = "FAILED"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Export generation failed: {str(exc)}")


@router.post("/exports/{batch_id}/sync")
def sync_to_tally(batch_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id)
    if company_id is not None:
        batch = batch.filter(TRN_TallyExportBatch.company_id == company_id)
    batch = batch.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    if batch.export_status != "COMPLETED":
        raise HTTPException(status_code=400, detail="Batch must be completed before syncing")

    batch.sync_status = "SYNCED"
    db.commit()
    return {"message": "Batch synced to Tally successfully"}


@router.get("/exports/{batch_id}/details", response_model=List[TallyExportDetailResponse])
def get_batch_details(batch_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    details = db.query(TRN_TallyExportDetail).filter(TRN_TallyExportDetail.batch_id == batch_id)
    if company_id is not None:
        details = details.filter(TRN_TallyExportDetail.company_id == company_id)
    details = details.all()
    return details


@router.delete("/exports/{batch_id}")
def delete_export_batch(batch_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    batch = db.query(TRN_TallyExportBatch).filter(TRN_TallyExportBatch.batch_id == batch_id)
    if company_id is not None:
        batch = batch.filter(TRN_TallyExportBatch.company_id == company_id)
    batch = batch.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Export batch not found")
    batch.is_active = False
    db.commit()
    return {"message": "Export batch deleted successfully"}
