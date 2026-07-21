from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.transactions.models import TRN_Commission, TRN_Case, TRN_Revenue
from src.masters.models import MST_Connector
from src.security.auth import get_current_user

router = APIRouter(prefix="/api/masters/commission", tags=["Masters"], dependencies=[Depends(get_current_user), Depends(require_company_id)])

class CommissionCreate(BaseModel):
    case_id: int
    connector_id: int
    commission_date: date
    base_commission_amount: float
    bonus_commission_amount: float = 0.0
    gross_commission_amount: float
    gst_amount: float = 0.0
    tds_amount: float = 0.0
    net_amount: float
    payment_status: str = "PENDING"
    notes: Optional[str] = None

class CommissionUpdate(BaseModel):
    case_id: Optional[int] = None
    connector_id: Optional[int] = None
    commission_date: Optional[date] = None
    base_commission_amount: Optional[float] = None
    bonus_commission_amount: Optional[float] = None
    gross_commission_amount: Optional[float] = None
    gst_amount: Optional[float] = None
    tds_amount: Optional[float] = None
    net_amount: Optional[float] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class CommissionResponse(BaseModel):
    commission_id: int
    case_id: int
    case_number: Optional[str] = None
    connector_id: int
    connector_name: Optional[str] = None
    commission_date: date
    base_commission_amount: float
    bonus_commission_amount: float
    gross_commission_amount: float
    gst_amount: float
    tds_amount: float
    net_amount: float
    payment_status: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CommissionResponse])
def list_commission(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    case_id: Optional[int] = None,
    connector_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id()
    query = db.query(TRN_Commission).filter(TRN_Commission.is_active == True)
    if company_id is not None:
        query = query.filter(TRN_Commission.company_id == company_id)
    if case_id:
        query = query.filter(TRN_Commission.case_id == case_id)
    if connector_id:
        query = query.filter(TRN_Commission.connector_id == connector_id)
    if payment_status:
        query = query.filter(TRN_Commission.payment_status == payment_status)
    commissions = query.offset(skip).limit(limit).all()

    for comm in commissions:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id)
        if company_id is not None:
            case = case.filter(TRN_Case.company_id == company_id)
        case = case.first()
        if case:
            comm.case_number = case.case_number
        connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id)
        if company_id is not None:
            connector = connector.filter(MST_Connector.company_id == company_id)
        connector = connector.first()
        if connector:
            comm.connector_name = connector.full_name
    return commissions

@router.get("/{commission_id}", response_model=CommissionResponse)
def get_commission(commission_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id)
    if company_id is not None:
        comm = comm.filter(TRN_Commission.company_id == company_id)
    comm = comm.first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id)
    if company_id is not None:
        case = case.filter(TRN_Case.company_id == company_id)
    case = case.first()
    if case:
        comm.case_number = case.case_number
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id)
    if company_id is not None:
        connector = connector.filter(MST_Connector.company_id == company_id)
    connector = connector.first()
    if connector:
        comm.connector_name = connector.full_name
    return comm

@router.post("/", response_model=CommissionResponse)
def create_commission(commission_data: CommissionCreate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    case = db.query(TRN_Case).filter(TRN_Case.case_id == commission_data.case_id)
    if company_id is not None:
        case = case.filter(TRN_Case.company_id == company_id)
    case = case.first()
    if not case:
        raise HTTPException(status_code=400, detail="Case not found")
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == commission_data.connector_id)
    if company_id is not None:
        connector = connector.filter(MST_Connector.company_id == company_id)
    connector = connector.first()
    if not connector:
        raise HTTPException(status_code=400, detail="Connector not found")

    new_commission = TRN_Commission(
        company_id=company_id or 1,
        case_id=commission_data.case_id,
        connector_id=commission_data.connector_id,
        commission_date=commission_data.commission_date,
        base_commission_amount=commission_data.base_commission_amount,
        bonus_commission_amount=commission_data.bonus_commission_amount,
        gross_commission_amount=commission_data.gross_commission_amount,
        gst_amount=commission_data.gst_amount,
        tds_amount=commission_data.tds_amount,
        net_amount=commission_data.net_amount,
        payment_status=commission_data.payment_status,
        notes=commission_data.notes,
        is_active=True
    )
    db.add(new_commission)
    db.commit()
    db.refresh(new_commission)
    return new_commission

@router.put("/{commission_id}", response_model=CommissionResponse)
def update_commission(commission_id: int, commission_data: CommissionUpdate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id)
    if company_id is not None:
        comm = comm.filter(TRN_Commission.company_id == company_id)
    comm = comm.first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    for field, value in commission_data.model_dump(exclude_unset=True).items():
        setattr(comm, field, value)
    db.commit()
    db.refresh(comm)
    return comm

@router.delete("/{commission_id}")
def delete_commission(commission_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id)
    if company_id is not None:
        comm = comm.filter(TRN_Commission.company_id == company_id)
    comm = comm.first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    comm.is_active = False
    db.commit()
    return {"message": "Commission deleted"}

@router.post("/calculate/{case_id}")
def calculate_commission(case_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id)
    if company_id is not None:
        case = case.filter(TRN_Case.company_id == company_id)
    case = case.first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    revenue = db.query(TRN_Revenue).filter(TRN_Revenue.case_id == case_id)
    if company_id is not None:
        revenue = revenue.filter(TRN_Revenue.company_id == company_id)
    revenue = revenue.first()
    if not revenue:
        return {"error": "Revenue not found for this case. Please create revenue first."}

    connector_share = 0.50
    base_commission = revenue.net_amount * connector_share
    gst_rate = 0.18
    tds_rate = 0.10
    gst_amount = base_commission * gst_rate
    tds_amount = base_commission * tds_rate
    net_amount = base_commission + gst_amount - tds_amount

    return {
        "case_id": case_id,
        "case_number": case.case_number,
        "revenue_amount": revenue.net_amount,
        "connector_share": connector_share,
        "base_commission": base_commission,
        "gst_amount": gst_amount,
        "tds_amount": tds_amount,
        "net_amount": net_amount
    }
