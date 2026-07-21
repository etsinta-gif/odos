# src/masters/api/lender.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.masters.models import MST_Lender
from pydantic import BaseModel

router = APIRouter(prefix="/api/masters/lenders", tags=["Masters"])

class LenderCreate(BaseModel):
    lender_name: str
    pan: str
    gstin: Optional[str] = None
    lender_code: Optional[str] = None
    is_nbfc: Optional[bool] = False
    credit_rating: Optional[str] = None

class LenderUpdate(BaseModel):
    lender_name: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    lender_code: Optional[str] = None
    is_nbfc: Optional[bool] = None
    credit_rating: Optional[str] = None
    is_active: Optional[bool] = None

class LenderResponse(BaseModel):
    lender_id: int
    lender_name: str
    pan: str
    gstin: Optional[str]
    lender_code: Optional[str]
    is_nbfc: bool
    credit_rating: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[LenderResponse])
def list_lenders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MST_Lender).filter(MST_Lender.is_active == True)
    if search:
        query = query.filter(
            MST_Lender.lender_name.ilike(f"%{search}%") |
            MST_Lender.pan.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{lender_id}", response_model=LenderResponse)
def get_lender(lender_id: int, db: Session = Depends(get_db)):
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")
    return lender

@router.post("/", response_model=LenderResponse)
def create_lender(lender_data: LenderCreate, db: Session = Depends(get_db)):
    existing = db.query(MST_Lender).filter(MST_Lender.pan == lender_data.pan).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lender with this PAN already exists")

    new_lender = MST_Lender(
        lender_name=lender_data.lender_name,
        pan=lender_data.pan,
        gstin=lender_data.gstin,
        lender_code=lender_data.lender_code,
        is_nbfc=lender_data.is_nbfc,
        credit_rating=lender_data.credit_rating,
        is_active=True
    )
    db.add(new_lender)
    db.commit()
    db.refresh(new_lender)
    return new_lender

@router.put("/{lender_id}", response_model=LenderResponse)
def update_lender(lender_id: int, lender_data: LenderUpdate, db: Session = Depends(get_db)):
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")

    for field, value in lender_data.model_dump(exclude_unset=True).items():
        setattr(lender, field, value)

    db.commit()
    db.refresh(lender)
    return lender

@router.delete("/{lender_id}")
def delete_lender(lender_id: int, db: Session = Depends(get_db)):
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == lender_id).first()
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")
    lender.is_active = False
    db.commit()
    return {"message": "Lender deactivated successfully"}
