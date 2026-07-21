# src/masters/api/connector.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.masters.models import MST_Connector
from pydantic import BaseModel

router = APIRouter(prefix="/api/masters/connectors", tags=["Masters"])

class ConnectorCreate(BaseModel):
    connector_code: str
    full_name: str
    pan: Optional[str] = None
    gstin: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc: Optional[str] = None

class ConnectorUpdate(BaseModel):
    connector_code: Optional[str] = None
    full_name: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    ifsc: Optional[str] = None
    is_active: Optional[bool] = None

class ConnectorResponse(BaseModel):
    connector_id: int
    connector_code: Optional[str]
    full_name: str
    pan: Optional[str]
    gstin: Optional[str]
    bank_name: Optional[str]
    account_number: Optional[str]
    ifsc: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ConnectorResponse])
def list_connectors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MST_Connector).filter(MST_Connector.is_active == True)
    if search:
        query = query.filter(
            MST_Connector.full_name.ilike(f"%{search}%") |
            MST_Connector.connector_code.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{connector_id}", response_model=ConnectorResponse)
def get_connector(connector_id: int, db: Session = Depends(get_db)):
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    return connector

@router.post("/", response_model=ConnectorResponse)
def create_connector(connector_data: ConnectorCreate, db: Session = Depends(get_db)):
    new_connector = MST_Connector(
        connector_code=connector_data.connector_code,
        full_name=connector_data.full_name,
        pan=connector_data.pan,
        gstin=connector_data.gstin,
        bank_name=connector_data.bank_name,
        account_number=connector_data.account_number,
        ifsc=connector_data.ifsc,
        is_active=True
    )
    db.add(new_connector)
    db.commit()
    db.refresh(new_connector)
    return new_connector

@router.put("/{connector_id}", response_model=ConnectorResponse)
def update_connector(connector_id: int, connector_data: ConnectorUpdate, db: Session = Depends(get_db)):
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")

    for field, value in connector_data.model_dump(exclude_unset=True).items():
        setattr(connector, field, value)

    db.commit()
    db.refresh(connector)
    return connector

@router.delete("/{connector_id}")
def delete_connector(connector_id: int, db: Session = Depends(get_db)):
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == connector_id).first()
    if not connector:
        raise HTTPException(status_code=404, detail="Connector not found")
    connector.is_active = False
    db.commit()
    return {"message": "Connector deactivated successfully"}
