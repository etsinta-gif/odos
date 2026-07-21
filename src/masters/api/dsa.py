from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.tenant import get_current_company_id, require_company_id
from src.masters.models import MST_DSA
from src.security.auth import get_current_user

router = APIRouter(prefix="/api/masters/dsas", tags=["Masters"], dependencies=[Depends(get_current_user), Depends(require_company_id)])


class DSACreate(BaseModel):
    dsa_code: str
    dsa_name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    is_active: Optional[bool] = True


class DSAUpdate(BaseModel):
    dsa_code: Optional[str] = None
    dsa_name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    is_active: Optional[bool] = None


class DSAResponse(BaseModel):
    dsa_id: int
    dsa_code: str
    dsa_name: str
    contact_person: Optional[str]
    email: Optional[str]
    mobile: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/", response_model=List[DSAResponse])
def list_dsas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    company_id = get_current_company_id()
    query = db.query(MST_DSA).filter(MST_DSA.is_active == True)
    if company_id is not None:
        query = query.filter(MST_DSA.dsa_id == company_id)
    if search:
        query = query.filter(
            MST_DSA.dsa_code.ilike(f"%{search}%") | MST_DSA.dsa_name.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()


@router.get("/{dsa_id}", response_model=DSAResponse)
def get_dsa(dsa_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    dsa = db.query(MST_DSA).filter(MST_DSA.dsa_id == dsa_id)
    if company_id is not None:
        dsa = dsa.filter(MST_DSA.dsa_id == company_id)
    dsa = dsa.first()
    if not dsa:
        raise HTTPException(status_code=404, detail="DSA not found")
    return dsa


@router.post("", response_model=DSAResponse)
@router.post("/", response_model=DSAResponse)
def create_dsa(dsa_data: DSACreate, db: Session = Depends(get_db)):
    existing = db.query(MST_DSA).filter(MST_DSA.dsa_code == dsa_data.dsa_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="DSA with this code already exists")

    new_dsa = MST_DSA(
        dsa_code=dsa_data.dsa_code,
        dsa_name=dsa_data.dsa_name,
        contact_person=dsa_data.contact_person,
        email=dsa_data.email,
        mobile=dsa_data.mobile,
        is_active=True if dsa_data.is_active is None else dsa_data.is_active,
    )
    db.add(new_dsa)
    db.commit()
    db.refresh(new_dsa)
    return new_dsa


@router.put("/{dsa_id}", response_model=DSAResponse)
def update_dsa(dsa_id: int, dsa_data: DSAUpdate, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    dsa = db.query(MST_DSA).filter(MST_DSA.dsa_id == dsa_id)
    if company_id is not None:
        dsa = dsa.filter(MST_DSA.dsa_id == company_id)
    dsa = dsa.first()
    if not dsa:
        raise HTTPException(status_code=404, detail="DSA not found")

    for field, value in dsa_data.model_dump(exclude_unset=True).items():
        setattr(dsa, field, value)

    db.commit()
    db.refresh(dsa)
    return dsa


@router.delete("/{dsa_id}")
def delete_dsa(dsa_id: int, db: Session = Depends(get_db)):
    company_id = get_current_company_id()
    dsa = db.query(MST_DSA).filter(MST_DSA.dsa_id == dsa_id)
    if company_id is not None:
        dsa = dsa.filter(MST_DSA.dsa_id == company_id)
    dsa = dsa.first()
    if not dsa:
        raise HTTPException(status_code=404, detail="DSA not found")
    dsa.is_active = False
    db.commit()
    return {"message": "DSA deactivated successfully"}
