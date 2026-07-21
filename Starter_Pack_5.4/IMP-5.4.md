# IMP-5.4 – Revenue & Commission Processing (UI & API)

**Document ID:** IMP-5.4
**Version:** 1.0
**Status:** Draft
**Owner:** Aniket
**Sprint:** 5.4
**Phase:** Phase 5 – Operational ERP
**Estimated Duration:** 2 days

---

## Sprint Overview

**Goal:** Build a system to manage Revenue (commission income from lenders) and Commission (payouts to connectors). This enables your Finance team to track income and manage payouts.

---

## Prerequisites

- [ ] Sprint 5.2 completed (Case Management UI)
- [ ] `TRN_Revenue` and `TRN_Commission` tables exist
- [ ] At least one case exists for testing
- [ ] `MST_Lender`, `MST_Connector`, `MST_Product` tables populated

---

## Step 1: Create Revenue API Endpoints

Create `src/masters/api/revenue.py` with the following code:

```python
# src/masters/api/revenue.py
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import TRN_Revenue, TRN_Case
from src.masters.models import MST_Lender

router = APIRouter(prefix="/api/masters/revenue", tags=["Masters"])

# ---------- Pydantic Schemas ----------
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

# ---------- CRUD ----------
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
```

---

## Step 2: Create Commission API Endpoints

Create `src/masters/api/commission.py` with the following code:

```python
# src/masters/api/commission.py
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.transactions.models import TRN_Commission, TRN_Case, TRN_Revenue
from src.masters.models import MST_Connector

router = APIRouter(prefix="/api/masters/commission", tags=["Masters"])

# ---------- Pydantic Schemas ----------
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

# ---------- CRUD ----------
@router.get("/", response_model=List[CommissionResponse])
def list_commission(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    case_id: Optional[int] = None,
    connector_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Commission).filter(TRN_Commission.is_active == True)
    if case_id:
        query = query.filter(TRN_Commission.case_id == case_id)
    if connector_id:
        query = query.filter(TRN_Commission.connector_id == connector_id)
    if payment_status:
        query = query.filter(TRN_Commission.payment_status == payment_status)
    commissions = query.offset(skip).limit(limit).all()

    for comm in commissions:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id).first()
        if case:
            comm.case_number = case.case_number
        connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id).first()
        if connector:
            comm.connector_name = connector.full_name
    return commissions

@router.get("/{commission_id}", response_model=CommissionResponse)
def get_commission(commission_id: int, db: Session = Depends(get_db)):
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id).first()
    if case:
        comm.case_number = case.case_number
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id).first()
    if connector:
        comm.connector_name = connector.full_name
    return comm

@router.post("/", response_model=CommissionResponse)
def create_commission(commission_data: CommissionCreate, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == commission_data.case_id).first()
    if not case:
        raise HTTPException(status_code=400, detail="Case not found")
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == commission_data.connector_id).first()
    if not connector:
        raise HTTPException(status_code=400, detail="Connector not found")

    new_commission = TRN_Commission(
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
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    for field, value in commission_data.model_dump(exclude_unset=True).items():
        setattr(comm, field, value)
    db.commit()
    db.refresh(comm)
    return comm

@router.delete("/{commission_id}")
def delete_commission(commission_id: int, db: Session = Depends(get_db)):
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    comm.is_active = False
    db.commit()
    return {"message": "Commission deleted"}

@router.post("/calculate/{case_id}")
def calculate_commission(case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    revenue = db.query(TRN_Revenue).filter(TRN_Revenue.case_id == case_id).first()
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
```

---

## Step 3: Extend UI Routes

Add Revenue and Commission UI routes to `src/masters/ui/routes.py` after the existing case routes. Copy the following after the last case route functions:

```python
from datetime import date
from typing import Optional

from fastapi import HTTPException
from src.transactions.models import TRN_Revenue, TRN_Commission, TRN_Case
from src.masters.models import MST_Lender, MST_Connector, MST_Customer
```

Then append the Revenue and Commission UI endpoint definitions exactly as described in the specification above.

---

## Step 4: Create HTML Templates

Add these new templates under `src/templates/masters/`:
- `revenue_list.html`
- `revenue_form.html`
- `revenue_detail.html`
- `commission_list.html`
- `commission_form.html`
- `commission_detail.html`

Also update `src/templates/masters/base.html` to add navigation links for Revenue and Commission.

---

## Step 5: Add CSS for Additional Status Badges

Append to `src/static/css/style.css`:

```css
.status-pending { background-color: #f39c12; color: white; }
.status-paid { background-color: #2ecc71; color: white; }
.status-failed { background-color: #e74c3c; color: white; }
.status-reconciled { background-color: #3498db; color: white; }

small a {
    color: #3498db;
    text-decoration: underline;
}
small a:hover {
    color: #2980b9;
}
```

---

## Step 6: Create Seed Script

Create `scripts/seed_test_revenue_commission.py` with optional sample data. Use it after existing case and connector records are present.

---

## Step 7: Test Your Work

Start the server with:

```bash
uvicorn src.main:app --reload
```

Then test:
- `http://localhost:8000/masters/revenue`
- `http://localhost:8000/masters/commission`
- `/api/masters/revenue`
- `/api/masters/commission`

---

## Notes

- Revenue and commission auto-calculation is simplified for starter pack purposes.
- If tables or models are missing, add them in the database schema and run migrations.
- Use the seed script only after cases and connectors exist.
