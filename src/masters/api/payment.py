from datetime import datetime, date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.transactions.models import TRN_Payment
from src.masters.models import MST_CompanyBankAccount
from src.security.auth import get_current_user

router = APIRouter(prefix="/api/masters/payments", tags=["Masters"], dependencies=[Depends(get_current_user), Depends(require_company_id)])

class PaymentCreate(BaseModel):
    payment_date: date
    company_bank_account_id: int
    payment_amount: float
    payment_mode: str
    utr_number: Optional[str] = None
    payment_type: str
    reference_id: int
    notes: Optional[str] = None

class PaymentUpdate(BaseModel):
    payment_date: Optional[date] = None
    company_bank_account_id: Optional[int] = None
    payment_amount: Optional[float] = None
    payment_mode: Optional[str] = None
    utr_number: Optional[str] = None
    payment_type: Optional[str] = None
    reference_id: Optional[int] = None
    reconciliation_status: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class PaymentResponse(BaseModel):
    payment_id: int
    payment_number: Optional[str]
    payment_date: date
    company_bank_account_id: int
    bank_name: Optional[str] = None
    payment_amount: float
    payment_mode: str
    utr_number: Optional[str]
    payment_type: str
    reference_id: int
    reconciliation_status: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[PaymentResponse])
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    payment_type: Optional[str] = None,
    reference_id: Optional[int] = None,
    reconciliation_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id()
    query = db.query(TRN_Payment).filter(TRN_Payment.is_active == True)
    if company_id is not None:
        query = query.filter(TRN_Payment.company_id == company_id)
    if payment_type:
        query = query.filter(TRN_Payment.payment_type == payment_type)
    if reference_id:
        query = query.filter(TRN_Payment.reference_id == reference_id)
    if reconciliation_status:
        query = query.filter(TRN_Payment.reconciliation_status == reconciliation_status)
    payments = query.offset(skip).limit(limit).all()

    for payment in payments:
        bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id)
        if company_id is not None:
            bank = bank.filter(MST_CompanyBankAccount.company_id == company_id)
        bank = bank.first()
        payment.bank_name = bank.bank_name if bank else None
    return payments

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id)
    if company_id is not None:
        payment = payment.filter(TRN_Payment.company_id == company_id)
    payment = payment.first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id)
    if company_id is not None:
        bank = bank.filter(MST_CompanyBankAccount.company_id == company_id)
    bank = bank.first()
    payment.bank_name = bank.bank_name if bank else None
    return payment

@router.post("/", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment_data.company_bank_account_id)
    if company_id is not None:
        bank = bank.filter(MST_CompanyBankAccount.company_id == company_id)
    bank = bank.first()
    if not bank:
        raise HTTPException(status_code=400, detail="Bank account not found")
    if payment_data.utr_number:
        existing = db.query(TRN_Payment).filter(TRN_Payment.utr_number == payment_data.utr_number)
        if company_id is not None:
            existing = existing.filter(TRN_Payment.company_id == company_id)
        existing = existing.first()
        if existing:
            raise HTTPException(status_code=400, detail="UTR number already exists")

    payment_number = f"PAY-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    new_payment = TRN_Payment(
        company_id=company_id or 1,
        payment_number=payment_number,
        payment_date=payment_data.payment_date,
        company_bank_account_id=payment_data.company_bank_account_id,
        payment_amount=payment_data.payment_amount,
        payment_mode=payment_data.payment_mode,
        utr_number=payment_data.utr_number,
        payment_type=payment_data.payment_type,
        reference_id=payment_data.reference_id,
        reconciliation_status="PENDING",
        notes=payment_data.notes,
        is_active=True
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment_data: PaymentUpdate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id)
    if company_id is not None:
        payment = payment.filter(TRN_Payment.company_id == company_id)
    payment = payment.first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment_data.utr_number and payment_data.utr_number != payment.utr_number:
        existing = db.query(TRN_Payment).filter(TRN_Payment.utr_number == payment_data.utr_number)
        if company_id is not None:
            existing = existing.filter(TRN_Payment.company_id == company_id)
        existing = existing.first()
        if existing:
            raise HTTPException(status_code=400, detail="UTR number already exists")
    for field, value in payment_data.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id)
    if company_id is not None:
        payment = payment.filter(TRN_Payment.company_id == company_id)
    payment = payment.first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.is_active = False
    db.commit()
    return {"message": "Payment deleted"}

@router.post("/{payment_id}/reconcile")
def reconcile_payment(payment_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id)
    if company_id is not None:
        payment = payment.filter(TRN_Payment.company_id == company_id)
    payment = payment.first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.reconciliation_status = "RECONCILED"
    db.commit()
    return {"message": "Payment reconciled successfully"}

@router.get("/reconciliation/pending")
def get_pending_reconciliation(db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    pending = db.query(TRN_Payment).filter(
        TRN_Payment.is_active == True,
        TRN_Payment.reconciliation_status == "PENDING"
    )
    if company_id is not None:
        pending = pending.filter(TRN_Payment.company_id == company_id)
    pending = pending.all()
    return pending
