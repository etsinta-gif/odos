# IMP-5.1 – Master Data Management (UI & API)

**Document ID:** IMP-5.1
**Version:** 1.0
**Status:** Draft
**Owner:** Aniket
**Sprint:** 5.1
**Phase:** Phase 5 – Operational ERP
**Estimated Duration:** 2–3 days

---

## Sprint Overview

**Goal:** Build a user-friendly web interface (UI) for managing master data. Your Ops and Finance teams will use these screens to add, view, edit, and deactivate Customers, Lenders, Products, Employees, and Connectors.

---

## Prerequisites

- [ ] Phase 1-4 completed (backend, database, APIs)
- [ ] MST_* tables exist (MST_Customer, MST_Lender, MST_Product, MST_Employee, MST_Connector)
- [ ] FastAPI server runs (uvicorn src.main:app --reload)

---

## Step 1: Install Required Packages

Before we start, we need to install `jinja2` for HTML templating (if not already installed).

1. Open VS Code and open the `odos` folder.
2. Open the terminal (View → Terminal or press `Ctrl+` `).
3. Activate your virtual environment:
   ```
   > source .venv/bin/activate
   ```
   (On Windows: `.venv\Scripts\activate`)
4. Install Jinja2:
   ```
   > uv pip install jinja2
   ```

---

## Step 2: Update Main App to Serve Templates and Static Files

We need to tell FastAPI where to find HTML templates and CSS/JS files.

1. Open `src/main.py` (or wherever your FastAPI app is created).
2. Add these imports at the top:
```python
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
```
3. Add these lines after creating the `app` instance:
```python
# Templates directory
templates = Jinja2Templates(directory="src/templates")

# Static files (CSS, JS)
app.mount("/static", StaticFiles(directory="src/static"), name="static")
```
4. Your `main.py` should look something like this:

```python
# src/main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.core.database import engine, Base
from src.security.api import auth
from src.masters.api import customer, lender, product, employee, connector
from src.masters.ui import routes as ui_routes

app = FastAPI(title="ODOS Enterprise Platform")

# Templates
templates = Jinja2Templates(directory="src/templates")

# Static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(lender.router)
app.include_router(product.router)
app.include_router(employee.router)
app.include_router(connector.router)
app.include_router(ui_routes.router)

@app.get("/")
def root():
    return {"message": "ODOS Enterprise Platform"}
```

---

## Step 3: Create API Endpoints (if not already exist)

The UI will call these APIs to perform CRUD operations. If your Phase 1 already created these, you can skip this step. If not, create them.

### 3.1 Customer API (`src/masters/api/customer.py`)

Create the file and paste:

```python
# src/masters/api/customer.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.masters.models import MST_Customer
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/api/masters/customers", tags=["Masters"])

# Pydantic schemas
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
    query = db.query(MST_Customer).filter(MST_Customer.is_active == True)
    if search:
        query = query.filter(
            MST_Customer.full_name.ilike(f"%{search}%") |
            MST_Customer.pan.ilike(f"%{search}%")
        )
    return query.offset(skip).limit(limit).all()

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/", response_model=CustomerResponse)
def create_customer(customer_data: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(MST_Customer).filter(MST_Customer.pan == customer_data.pan).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer with this PAN already exists")

    new_customer = MST_Customer(
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
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for field, value in customer_data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(MST_Customer).filter(MST_Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.is_active = False
    db.commit()
    return {"message": "Customer deactivated successfully"}
```

### 3.2 Lender, Product, Employee, Connector APIs

Follow the exact same pattern as Customer API but change the model names and fields. Create files:

- `src/masters/api/lender.py`
- `src/masters/api/product.py`
- `src/masters/api/employee.py`
- `src/masters/api/connector.py`

Use the same CRUD structure, response models, and soft-delete logic.

---

## Step 4: Create the Base HTML Template

Create `src/templates/masters/base.html` with the shared layout.

---

## Step 5: Create UI Routes

UI routes render HTML pages and use the API functions for backend operations.

Create `src/masters/ui/routes.py` and implement CRUD pages for all five entities.

---

## Step 6: Create HTML Templates

Create list and form templates for:
- `customer_list.html`
- `customer_form.html`
- `lender_list.html`
- `lender_form.html`
- `product_list.html`
- `product_form.html`
- `employee_list.html`
- `employee_form.html`
- `connector_list.html`
- `connector_form.html`

Follow the Customer examples and replace entity-specific fields.

---

## Step 7: Create CSS Styling

Create `src/static/css/style.css` with the provided styles.

---

## Step 8: Test Your Work

Start the server and verify the UI at `http://localhost:8000/masters/customers`.

---

## FCPL Test Scenario Summary

These FCPL-specific tests cover the extended master data requirements for connectors, lenders, and products.

- **Connector Full Details:** Connector create/edit must capture `Connector Code`, `PAN`, `GSTIN`, `Bank Name`, `Account Number`, `IFSC`, and `Unit Head`.
- **Connector PAN Validation:** Duplicate `PAN` values must be blocked for connectors.
- **Lender NBFC Flag:** Lenders such as `Tata Capital` must support `is_nbfc=true`.
- **Product Association:** Products such as `Business Loan` must link to a lender and support categories like `BL` / `PL` / `LAP`.
- **Connector Hierarchy:** Parent-child connector grouping should be supported in UI/listing.

---

## Acceptance Criteria Checklist

- [ ] `http://localhost:8000/masters/customers` shows a list of customers.
- [ ] Clicking "Add Customer" opens a form.
- [ ] Submitting the form creates a new customer in `MST_Customer`.
- [ ] Clicking "Edit" opens the form with pre-filled data.
- [ ] Submitting the edit updates the customer.
- [ ] Clicking "Delete" soft-deletes the customer (sets `is_active=False`).
- [ ] The same CRUD logic works for Lenders, Products, Employees, and Connectors.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `jinja2` not found | Run `uv pip install jinja2` |
| Templates not found | Ensure `src/templates/` is in the correct location. |
| 404 Not Found | Check that the router is included in `main.py`. |
| Form submission fails | Check the API endpoints exist in `src/masters/api/`. |
| CSS not loading | Ensure `src/static/` is mounted correctly. |
