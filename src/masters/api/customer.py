# src/masters/api/customer.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.masters.models import MST_Customer
from src.security.auth import get_current_user
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/masters/customers", tags=["Masters"], dependencies=[Depends(get_current_user), Depends(require_company_id)])

class CustomerCreate(BaseModel):
    full_name: str
    pan: str
    gstin: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    date_of_birth: Optional[date] = None
    occupation: Optional[str] = None
    annual_income: Optional[float] = None

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    date_of_birth: Optional[date] = None
    occupation: Optional[str] = None
    annual_income: Optional[float] = None
    is_active: Optional[bool] = None

class CustomerResponse(BaseModel):
    customer_id: int
    full_name: str
    pan: str
    gstin: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    date_of_birth: Optional[date]
    occupation: Optional[str]
    annual_income: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CustomerResponse])
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    company_id = get_current_company_id()
    query = db.query(MST_Customer).filter(MST_Customer.is_active == True)
    if company_id is not None:
        query = query.filter(MST_Customer.company_id == company_id)
    if search:
        query = query.filter(
            MST_Customer.full_name.ilike(f"%{search}%") |
            MST_Customer.pan.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id)
    if company_id is not None:
        customer = customer.filter(MST_Customer.company_id == company_id)
    customer = customer.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("", response_model=CustomerResponse)
@router.post("/", response_model=CustomerResponse)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    existing = db.query(MST_Customer).filter(MST_Customer.pan == customer_data.pan)
    if company_id is not None:
        existing = existing.filter(MST_Customer.company_id == company_id)
    existing = existing.first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this PAN already exists")

    new_customer = MST_Customer(
        company_id=company_id or 1,
        full_name=customer_data.full_name,
        pan=customer_data.pan,
        gstin=customer_data.gstin,
        email=customer_data.email,
        mobile=customer_data.mobile,
        date_of_birth=customer_data.date_of_birth,
        occupation=customer_data.occupation,
        annual_income=customer_data.annual_income,
        is_active=True
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer_data: CustomerUpdate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id)
    if company_id is not None:
        customer = customer.filter(MST_Customer.company_id == company_id)
    customer = customer.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for field, value in customer_data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id)
    if company_id is not None:
        customer = customer.filter(MST_Customer.company_id == company_id)
    customer = customer.first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = False
    db.commit()
    return {"message": "Customer deactivated successfully"}
