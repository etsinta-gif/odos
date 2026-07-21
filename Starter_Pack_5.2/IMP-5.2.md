# IMP-5.2 – Case Management (UI & API)

**Document ID:** IMP-5.2
**Version:** 1.0
**Status:** Draft
**Owner:** Aniket
**Sprint:** 5.2
**Phase:** Phase 5 – Operational ERP
**Estimated Duration:** 2 days

---

## Sprint Overview

**Goal:** Build a user-friendly web interface to manage Loan Cases. Users can list, create, edit, view details, and change the status of cases (e.g., Lead → Application → Sanctioned → Disbursed → Closed). This is the core operational screen for your Ops team.

---

## Prerequisites

- [ ] Sprint 5.1 completed (Master Data Management UI)
- [ ] `MST_Customer`, `MST_Lender`, `MST_Product` tables have at least one record each
- [ ] `TRN_Case` and `TRN_CaseStatusHistory` tables exist (created in Phase 1)
- [ ] FastAPI server runs with Jinja2 templates

---

## Step 1: Create Case API Endpoints

If you don't already have Case CRUD APIs, create them now. We'll need endpoints for:
- List cases (with search/filter)
- Get single case
- Create case
- Update case
- Soft delete case
- Transition status (optional)

Create `src/masters/api/case.py` with the following code:

```python
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

# ---------- Pydantic Schemas ----------
class CaseCreate(BaseModel):
    customer_id: int
    lender_id: int
    product_id: int
    application_date: Optional[date] = None
    sanction_date: Optional[date] = None
    disbursement_date: Optional[date] = None
    sanction_amount: Optional[float] = None
    disbursement_amount: Optional[float] = None
    case_number: Optional[str] = None   # auto-generated if not provided
    status: str = "LEAD"                # default

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

# ---------- CRUD ----------
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

# ---------- Status Transition ----------
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
```

---

## Step 2: Extend UI Routes

Now add UI routes for Cases to `src/masters/ui/routes.py`. Keep all existing Sprint 5.1 routes and append the new case routes.

**Important:** If you already have this file, append only the new routes. If not, replace the file with the combined code carefully.

---

## Step 3: Create HTML Templates

Add `case_list.html`, `case_form.html`, and `case_detail.html` in `src/templates/masters/`, and update `base.html` to include Cases in navigation.

---

## Step 4: Add CSS for Status Badges

Append badge styles to `src/static/css/style.css`.

---

## Step 5: Test Your Work

Start the server and verify `http://localhost:8000/masters/cases`.

---

## FCPL Test Scenario Summary

These FCPL-specific tests cover case management requirements for loan cases, payout splits, and status workflows.

- **Case Creation with Connector Split:** Cases should support multiple connector pays and payout percentages.
- **Processing Fee Parsing:** Values like `30000(3%)` must be parsed into numeric amount and percentage.
- **Tenure Parsing:** Mixed formats such as `36M`, `2+4`, and `12+36` must be handled consistently.
- **Status Workflow:** Status transitions like `LOGIN DONE - IN PROCESS`, `APPROVED`, `SANCTIONED`, `DISBURSED`, and `CLOSED` must be tracked with history.
- **Bank Payout %:** Case detail/list should reflect the correct lender payout percentage from configured slabs.

---

## Acceptance Criteria Checklist

- [ ] `http://localhost:8000/masters/cases` shows a list of cases.
- [ ] "Add Case" form works and creates a new case in `TRN_Case`.
- [ ] "View" shows all details and allows status transition.
- [ ] Status transition updates the case status and logs history.
- [ ] "Edit" updates fields and saves.
- [ ] "Delete" soft-deletes (sets `is_active=False`).

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Dropdowns empty | Ensure you have at least one Customer, Lender, Product record. |
| Foreign key violation | Make sure the selected IDs exist in the parent tables. |
| Status transition fails | Check that the API endpoint `/api/masters/cases/{id}/status` exists. |
| `TRN_CaseStatusHistory` missing | Create the table if not present (run migrations). |
| `case_number` generation | Auto-generation uses timestamp; if you prefer a different format, modify the logic. |
