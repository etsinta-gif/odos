# src/masters/api/case.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.transactions.models import TRN_Case, TRN_CaseStatusHistory
from src.masters.models import MST_Customer, MST_Lender, MST_Product
from pydantic import BaseModel
from datetime import date, datetime

router = APIRouter(prefix="/api/masters/cases", tags=["Masters"])

class CaseCreate(BaseModel):
    customer_id: int
    lender_id: int
    product_id: int
    application_date: Optional[date] = None
    sanction_date: Optional[date] = None
    disbursement_date: Optional[date] = None
    sanction_amount: Optional[float] = None
    disbursement_amount: Optional[float] = None
    case_number: Optional[str] = None
    status: str = "LEAD"

class CaseUpdate(BaseModel):
    customer_id: Optional[int] = None
    lender_id: Optional[int] = None
    product_id: Optional[int] = None
    application_date: Optional[date] = None
    sanction_date: Optional[date] = None
    disbursement_date: Optional[date] = None
    sanction_amount: Optional[float] = None
    disbursement_amount: Optional[float] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None

class CaseResponse(BaseModel):
    case_id: int
    case_number: str
    customer_id: int
    lender_id: int
    product_id: int
    application_date: Optional[date]
    sanction_date: Optional[date]
    disbursement_date: Optional[date]
    sanction_amount: Optional[float]
    disbursement_amount: Optional[float]
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CaseResponse])
def list_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Case).filter(TRN_Case.is_active == True)
    if search:
        query = query.filter(
            TRN_Case.case_number.ilike(f"%{search}%") |
            TRN_Case.case_id.cast(str).ilike(f"%{search}%")
        )
    if status:
        query = query.filter(TRN_Case.status == status)
    return query.offset(skip).limit(limit).all()

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/", response_model=CaseResponse)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == case_data.customer_id).first()
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == case_data.lender_id).first()
    product = db.query(MST_Product).filter(MST_Product.product_id == case_data.product_id).first()
    if not customer or not lender or not product:
        raise HTTPException(status_code=400, detail="Invalid customer, lender, or product ID")

    case_number = case_data.case_number or f"FY{datetime.now().strftime('%y')}-{int(datetime.now().strftime('%y'))+1}/SC/{datetime.now().strftime('%m%d%H%M%S')}"

    new_case = TRN_Case(
        case_number=case_number,
        customer_id=case_data.customer_id,
        lender_id=case_data.lender_id,
        product_id=case_data.product_id,
        application_date=case_data.application_date,
        sanction_date=case_data.sanction_date,
        disbursement_date=case_data.disbursement_date,
        sanction_amount=case_data.sanction_amount,
        disbursement_amount=case_data.disbursement_amount,
        status=case_data.status,
        is_active=True
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    status_history = TRN_CaseStatusHistory(
        case_id=new_case.case_id,
        status=case_data.status,
        changed_at=datetime.utcnow()
    )
    db.add(status_history)
    db.commit()

    return new_case

@router.put("/{case_id}", response_model=CaseResponse)
def update_case(case_id: int, case_data: CaseUpdate, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    for field, value in case_data.model_dump(exclude_unset=True).items():
        setattr(case, field, value)
    db.commit()
    db.refresh(case)
    return case

@router.delete("/{case_id}")
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case.is_active = False
    db.commit()
    return {"message": "Case deactivated"}

@router.post("/{case_id}/status")
def transition_status(case_id: int, new_status: str, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    case.status = new_status
    db.commit()
    history = TRN_CaseStatusHistory(
        case_id=case.case_id,
        status=new_status,
        changed_at=datetime.utcnow()
    )
    db.add(history)
    db.commit()
    return {"message": f"Status updated to {new_status}"}
