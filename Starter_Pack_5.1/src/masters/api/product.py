# src/masters/api/product.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.masters.models import MST_Product
from pydantic import BaseModel

router = APIRouter(prefix="/api/masters/products", tags=["Masters"])

class ProductCreate(BaseModel):
    product_name: str
    product_code: Optional[str] = None
    lender_id: Optional[int] = None
    interest_rate: Optional[float] = None
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    product_code: Optional[str] = None
    lender_id: Optional[int] = None
    interest_rate: Optional[float] = None
    min_loan_amount: Optional[float] = None
    max_loan_amount: Optional[float] = None
    is_active: Optional[bool] = None

class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    product_code: Optional[str]
    lender_id: Optional[int]
    interest_rate: Optional[float]
    min_loan_amount: Optional[float]
    max_loan_amount: Optional[float]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MST_Product).filter(MST_Product.is_active == True)
    if search:
        query = query.filter(
            MST_Product.product_name.ilike(f"%{search}%") |
            MST_Product.product_code.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(MST_Product).filter(MST_Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    new_product = MST_Product(
        product_name=product_data.product_name,
        product_code=product_data.product_code,
        lender_id=product_data.lender_id,
        interest_rate=product_data.interest_rate,
        min_loan_amount=product_data.min_loan_amount,
        max_loan_amount=product_data.max_loan_amount,
        is_active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(MST_Product).filter(MST_Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(MST_Product).filter(MST_Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_active = False
    db.commit()
    return {"message": "Product deactivated successfully"}
