from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import TRN_Revenue, TRN_Case
from src.masters.models import MST_Lender

router = APIRouter(prefix="/api/masters/revenue", tags=["Masters"])

class RevenueCreate(BaseModel):
    case_id: int
    revenue_date: date
    base_revenue_amount: float
    gst_amount: float = 0.0
    tds_amount: float = 0.0
    net_amount: float
    utr_number: Optional[str] = None
    payment_status: str = "PENDING"
    notes: Optional[str] = None

class RevenueUpdate(BaseModel):
    revenue_date: Optional[date] = None
    base_revenue_amount: Optional[float] = None
    gst_amount: Optional[float] = None
    tds_amount: Optional[float] = None
    net_amount: Optional[float] = None
    utr_number: Optional[str] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class RevenueResponse(BaseModel):
    revenue_id: int
    case_id: int
    case_number: Optional[str] = None
    lender_name: Optional[str] = None
    revenue_date: date
    base_revenue_amount: float
    gst_amount: float
    tds_amount: float
    net_amount: float
    utr_number: Optional[str]
    payment_status: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[RevenueResponse])
def list_revenue(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    case_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Revenue).filter(TRN_Revenue.is_active == True)
    if case_id:
        query = query.filter(TRN_Revenue.case_id == case_id)
    if payment_status:
        query = query.filter(TRN_Revenue.payment_status == payment_status)
    revenues = query.offset(skip).limit(limit).all()

    for rev in revenues:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == rev.case_id).first()
        if case:
            rev.case_number = case.case_number
            lender = db.query(MST_Lender).filter(MST_Lender.lender_id == case.lender_id).first()
            rev.lender_name = lender.lender_name if lender else None
    return revenues

@router.get("/{revenue_id}", response_model=RevenueResponse)
def get_revenue(revenue_id: int, db: Session = Depends(get_db)):
    rev = db.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revenue not found")
    case = db.query(TRN_Case).filter(TRN_Case.case_id == rev.case_id).first()
    if case:
        rev.case_number = case.case_number
        lender = db.query(MST_Lender).filter(MST_Lender.lender_id == case.lender_id).first()
        rev.lender_name = lender.lender_name if lender else None
    return rev

@router.post("/", response_model=RevenueResponse)
def create_revenue(revenue_data: RevenueCreate, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == revenue_data.case_id).first()
    if not case:
        raise HTTPException(status_code=400, detail="Case not found")

    new_revenue = TRN_Revenue(
        case_id=revenue_data.case_id,
        revenue_date=revenue_data.revenue_date,
        base_revenue_amount=revenue_data.base_revenue_amount,
        gst_amount=revenue_data.gst_amount,
        tds_amount=revenue_data.tds_amount,
        net_amount=revenue_data.net_amount,
        utr_number=revenue_data.utr_number,
        payment_status=revenue_data.payment_status,
        notes=revenue_data.notes,
        is_active=True
    )
    db.add(new_revenue)
    db.commit()
    db.refresh(new_revenue)
    return new_revenue

@router.put("/{revenue_id}", response_model=RevenueResponse)
def update_revenue(revenue_id: int, revenue_data: RevenueUpdate, db: Session = Depends(get_db)):
    rev = db.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revenue not found")
    for field, value in revenue_data.model_dump(exclude_unset=True).items():
        setattr(rev, field, value)
    db.commit()
    db.refresh(rev)
    return rev

@router.delete("/{revenue_id}")
def delete_revenue(revenue_id: int, db: Session = Depends(get_db)):
    rev = db.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revenue not found")
    rev.is_active = False
    db.commit()
    return {"message": "Revenue deleted"}

@router.post("/calculate/{case_id}")
def calculate_revenue(case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    commission_rate = 0.025
    base_amount = case.disbursement_amount or case.sanction_amount or 0
    base_revenue = base_amount * commission_rate
    gst_rate = 0.18
    tds_rate = 0.10
    gst_amount = base_revenue * gst_rate
    tds_amount = base_revenue * tds_rate
    net_amount = base_revenue + gst_amount - tds_amount

    return {
        "case_id": case_id,
        "case_number": case.case_number,
        "disbursement_amount": base_amount,
        "commission_rate": commission_rate,
        "base_revenue": base_revenue,
        "gst_amount": gst_amount,
        "tds_amount": tds_amount,
        "net_amount": net_amount
    }
