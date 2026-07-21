# src/masters/api/employee.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.masters.models import MST_Employee
from pydantic import BaseModel

router = APIRouter(prefix="/api/masters/employees", tags=["Masters"])

class EmployeeCreate(BaseModel):
    employee_code: str
    full_name: str
    designation: Optional[str] = None
    department: Optional[str] = None
    branch_id: Optional[int] = None
    email: Optional[str] = None
    mobile: Optional[str] = None

class EmployeeUpdate(BaseModel):
    employee_code: Optional[str] = None
    full_name: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    branch_id: Optional[int] = None
    email: Optional[str] = None
    mobile: Optional[str] = None
    is_active: Optional[bool] = None

class EmployeeResponse(BaseModel):
    employee_id: int
    employee_code: Optional[str]
    full_name: str
    designation: Optional[str]
    department: Optional[str]
    branch_id: Optional[int]
    email: Optional[str]
    mobile: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(MST_Employee).filter(MST_Employee.is_active == True)
    if search:
        query = query.filter(
            MST_Employee.full_name.ilike(f"%{search}%") |
            MST_Employee.employee_code.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(MST_Employee).filter(MST_Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", response_model=EmployeeResponse)
def create_employee(employee_data: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = MST_Employee(
        employee_code=employee_data.employee_code,
        full_name=employee_data.full_name,
        designation=employee_data.designation,
        department=employee_data.department,
        branch_id=employee_data.branch_id,
        email=employee_data.email,
        mobile=employee_data.mobile,
        is_active=True
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee_data: EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(MST_Employee).filter(MST_Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for field, value in employee_data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(MST_Employee).filter(MST_Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee.is_active = False
    db.commit()
    return {"message": "Employee deactivated successfully"}
