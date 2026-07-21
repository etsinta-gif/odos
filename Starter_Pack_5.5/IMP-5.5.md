# IMP-5.5 – Expense & Payment Management (UI & API)

**Document ID:** IMP-5.5
**Version:** 1.0
**Status:** Draft
**Owner:** Aniket
**Sprint:** 5.5
**Phase:** Phase 5 – Operational ERP
**Estimated Duration:** 2 days

---

## Sprint Overview

**Goal:** Build a system to manage operational expenses (including recurring expenses and claims) and outbound payments (with UTR tracking and bank reconciliation). This enables your Finance team to track all outflows and reconcile bank statements.

---

## Prerequisites

- [ ] Sprint 5.4 completed (Revenue & Commission Processing UI)
- [ ] `TRN_Expense`, `TRN_RecurringExpense`, `TRN_ExpenseClaim`, `TRN_Payment` tables exist
- [ ] `MST_Vendor`, `MST_ExpenseCategory`, `MST_CostCenter`, `MST_CompanyBankAccount` tables exist
- [ ] At least one vendor, expense category, and cost centre exist

---

## Step 1: Create Expense API Endpoints

Create `src/masters/api/expense.py` with the following code:

```python
# src/masters/api/expense.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.transactions.models import TRN_Expense, TRN_RecurringExpense, TRN_ExpenseClaim, TRN_Case
from src.masters.models import MST_Vendor, MST_ExpenseCategory, MST_CostCenter
from pydantic import BaseModel
from datetime import date, datetime

router = APIRouter(prefix="/api/masters/expenses", tags=["Masters"])

# ---------- Pydantic Schemas ----------
class ExpenseCreate(BaseModel):
    expense_date: date
    vendor_id: Optional[int] = None
    expense_category_id: int
    cost_center_id: Optional[int] = None
    case_id: Optional[int] = None
    description: str
    amount: float
    gst_amount: float = 0.0
    tds_amount: float = 0.0
    net_amount: float
    payment_status: str = "PENDING"
    invoice_reference: Optional[str] = None
    notes: Optional[str] = None

class ExpenseUpdate(BaseModel):
    expense_date: Optional[date] = None
    vendor_id: Optional[int] = None
    expense_category_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    case_id: Optional[int] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    gst_amount: Optional[float] = None
    tds_amount: Optional[float] = None
    net_amount: Optional[float] = None
    payment_status: Optional[str] = None
    invoice_reference: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class ExpenseResponse(BaseModel):
    expense_id: int
    expense_date: date
    vendor_id: Optional[int]
    vendor_name: Optional[str] = None
    expense_category_id: int
    expense_category_name: Optional[str] = None
    cost_center_id: Optional[int]
    cost_center_name: Optional[str] = None
    case_id: Optional[int]
    case_number: Optional[str] = None
    description: str
    amount: float
    gst_amount: float
    tds_amount: float
    net_amount: float
    payment_status: str
    invoice_reference: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ---------- CRUD ----------
@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    expense_category_id: Optional[int] = None,
    vendor_id: Optional[int] = None,
    case_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Expense).filter(TRN_Expense.is_active == True)
    if expense_category_id:
        query = query.filter(TRN_Expense.expense_category_id == expense_category_id)
    if vendor_id:
        query = query.filter(TRN_Expense.vendor_id == vendor_id)
    if case_id:
        query = query.filter(TRN_Expense.case_id == case_id)
    if payment_status:
        query = query.filter(TRN_Expense.payment_status == payment_status)
    expenses = query.offset(skip).limit(limit).all()
    
    for exp in expenses:
        vendor = db.query(MST_Vendor).filter(MST_Vendor.vendor_id == exp.vendor_id).first()
        exp.vendor_name = vendor.vendor_name if vendor else None
        category = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.expense_category_id == exp.expense_category_id).first()
        exp.expense_category_name = category.category_name if category else None
        cost_center = db.query(MST_CostCenter).filter(MST_CostCenter.cost_center_id == exp.cost_center_id).first()
        exp.cost_center_name = cost_center.center_name if cost_center else None
        if exp.case_id:
            case = db.query(TRN_Case).filter(TRN_Case.case_id == exp.case_id).first()
            exp.case_number = case.case_number if case else None
    return expenses

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    exp = db.query(TRN_Expense).filter(TRN_Expense.expense_id == expense_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    vendor = db.query(MST_Vendor).filter(MST_Vendor.vendor_id == exp.vendor_id).first()
    exp.vendor_name = vendor.vendor_name if vendor else None
    category = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.expense_category_id == exp.expense_category_id).first()
    exp.expense_category_name = category.category_name if category else None
    cost_center = db.query(MST_CostCenter).filter(MST_CostCenter.cost_center_id == exp.cost_center_id).first()
    exp.cost_center_name = cost_center.center_name if cost_center else None
    if exp.case_id:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == exp.case_id).first()
        exp.case_number = case.case_number if case else None
    return exp

@router.post("/", response_model=ExpenseResponse)
def create_expense(expense_data: ExpenseCreate, db: Session = Depends(get_db)):
    category = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.expense_category_id == expense_data.expense_category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Expense category not found")
    new_expense = TRN_Expense(
        expense_date=expense_data.expense_date,
        vendor_id=expense_data.vendor_id,
        expense_category_id=expense_data.expense_category_id,
        cost_center_id=expense_data.cost_center_id,
        case_id=expense_data.case_id,
        description=expense_data.description,
        amount=expense_data.amount,
        gst_amount=expense_data.gst_amount,
        tds_amount=expense_data.tds_amount,
        net_amount=expense_data.net_amount,
        payment_status=expense_data.payment_status,
        invoice_reference=expense_data.invoice_reference,
        notes=expense_data.notes,
        is_active=True
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: int, expense_data: ExpenseUpdate, db: Session = Depends(get_db)):
    exp = db.query(TRN_Expense).filter(TRN_Expense.expense_id == expense_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    for field, value in expense_data.model_dump(exclude_unset=True).items():
        setattr(exp, field, value)
    db.commit()
    db.refresh(exp)
    return exp

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    exp = db.query(TRN_Expense).filter(TRN_Expense.expense_id == expense_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expense not found")
    exp.is_active = False
    db.commit()
    return {"message": "Expense deleted"}

# ---------- Recurring Expenses ----------
class RecurringExpenseCreate(BaseModel):
    expense_category_id: int
    vendor_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    description: str
    amount: float
    gst_amount: float = 0.0
    tds_amount: float = 0.0
    net_amount: float
    frequency: str
    start_date: date
    end_date: Optional[date] = None
    invoice_reference: Optional[str] = None
    notes: Optional[str] = None

class RecurringExpenseResponse(BaseModel):
    recurring_expense_id: int
    expense_category_id: int
    vendor_id: Optional[int]
    cost_center_id: Optional[int]
    description: str
    amount: float
    gst_amount: float
    tds_amount: float
    net_amount: float
    frequency: str
    start_date: date
    end_date: Optional[date]
    invoice_reference: Optional[str]
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@router.get("/recurring", response_model=List[RecurringExpenseResponse])
def list_recurring_expenses(db: Session = Depends(get_db)):
    recurring = db.query(TRN_RecurringExpense).filter(TRN_RecurringExpense.is_active == True).all()
    return recurring

@router.post("/recurring", response_model=RecurringExpenseResponse)
def create_recurring_expense(data: RecurringExpenseCreate, db: Session = Depends(get_db)):
    new_recurring = TRN_RecurringExpense(
        expense_category_id=data.expense_category_id,
        vendor_id=data.vendor_id,
        cost_center_id=data.cost_center_id,
        description=data.description,
        amount=data.amount,
        gst_amount=data.gst_amount,
        tds_amount=data.tds_amount,
        net_amount=data.net_amount,
        frequency=data.frequency,
        start_date=data.start_date,
        end_date=data.end_date,
        invoice_reference=data.invoice_reference,
        notes=data.notes,
        is_active=True
    )
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    return new_recurring

@router.put("/recurring/{recurring_id}")
def update_recurring_expense(recurring_id: int, data: RecurringExpenseCreate, db: Session = Depends(get_db)):
    recurring = db.query(TRN_RecurringExpense).filter(TRN_RecurringExpense.recurring_expense_id == recurring_id).first()
    if not recurring:
        raise HTTPException(status_code=404, detail="Recurring expense not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(recurring, field, value)
    db.commit()
    db.refresh(recurring)
    return recurring

@router.delete("/recurring/{recurring_id}")
def delete_recurring_expense(recurring_id: int, db: Session = Depends(get_db)):
    recurring = db.query(TRN_RecurringExpense).filter(TRN_RecurringExpense.recurring_expense_id == recurring_id).first()
    if not recurring:
        raise HTTPException(status_code=404, detail="Recurring expense not found")
    recurring.is_active = False
    db.commit()
    return {"message": "Recurring expense deleted"}

@router.post("/recurring/generate/{recurring_id}")
def generate_expense_from_recurring(recurring_id: int, db: Session = Depends(get_db)):
    recurring = db.query(TRN_RecurringExpense).filter(TRN_RecurringExpense.recurring_expense_id == recurring_id).first()
    if not recurring:
        raise HTTPException(status_code=404, detail="Recurring expense not found")
    new_expense = TRN_Expense(
        expense_date=date.today(),
        vendor_id=recurring.vendor_id,
        expense_category_id=recurring.expense_category_id,
        cost_center_id=recurring.cost_center_id,
        description=f"{recurring.description} (auto-generated)",
        amount=recurring.amount,
        gst_amount=recurring.gst_amount,
        tds_amount=recurring.tds_amount,
        net_amount=recurring.net_amount,
        payment_status="PENDING",
        invoice_reference=recurring.invoice_reference,
        notes=f"Auto-generated from recurring #{recurring_id}",
        is_active=True
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"message": "Expense generated from recurring template", "expense_id": new_expense.expense_id}
```

---

## Step 2: Create Payment API Endpoints

Create `src/masters/api/payment.py` with the following code:

```python
# src/masters/api/payment.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.core.database import get_db
from src.transactions.models import TRN_Payment, TRN_Revenue, TRN_Commission, TRN_Expense
from src.masters.models import MST_CompanyBankAccount
from pydantic import BaseModel
from datetime import date, datetime

router = APIRouter(prefix="/api/masters/payments", tags=["Masters"])

# ---------- Pydantic Schemas ----------
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

# ---------- CRUD ----------
@router.get("/", response_model=List[PaymentResponse])
def list_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    payment_type: Optional[str] = None,
    reference_id: Optional[int] = None,
    reconciliation_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Payment).filter(TRN_Payment.is_active == True)
    if payment_type:
        query = query.filter(TRN_Payment.payment_type == payment_type)
    if reference_id:
        query = query.filter(TRN_Payment.reference_id == reference_id)
    if reconciliation_status:
        query = query.filter(TRN_Payment.reconciliation_status == reconciliation_status)
    payments = query.offset(skip).limit(limit).all()
    
    for payment in payments:
        bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id).first()
        payment.bank_name = bank.bank_name if bank else None
    return payments

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id).first()
    payment.bank_name = bank.bank_name if bank else None
    return payment

@router.post("/", response_model=PaymentResponse)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment_data.company_bank_account_id).first()
    if not bank:
        raise HTTPException(status_code=400, detail="Bank account not found")
    if payment_data.utr_number:
        existing = db.query(TRN_Payment).filter(TRN_Payment.utr_number == payment_data.utr_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="UTR number already exists")
    payment_number = f"PAY-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
    new_payment = TRN_Payment(
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
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment_data.utr_number and payment_data.utr_number != payment.utr_number:
        existing = db.query(TRN_Payment).filter(TRN_Payment.utr_number == payment_data.utr_number).first()
        if existing:
            raise HTTPException(status_code=400, detail="UTR number already exists")
    for field, value in payment_data.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.is_active = False
    db.commit()
    return {"message": "Payment deleted"}

@router.post("/{payment_id}/reconcile")
def reconcile_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.reconciliation_status = "RECONCILED"
    db.commit()
    return {"message": "Payment reconciled successfully"}

@router.get("/reconciliation/pending")
def get_pending_reconciliation(db: Session = Depends(get_db)):
    pending = db.query(TRN_Payment).filter(
        TRN_Payment.is_active == True,
        TRN_Payment.reconciliation_status == "PENDING"
    ).all()
    return pending
```

---

## Step 3: Extend UI Routes

Update `src/masters/ui/routes.py` with new expense and payment routes. Add these imports near the existing top imports:

```python
from src.transactions.models import TRN_Expense, TRN_RecurringExpense, TRN_Payment, TRN_Revenue, TRN_Commission, TRN_Case
from src.masters.models import MST_Vendor, MST_ExpenseCategory, MST_CostCenter, MST_CompanyBankAccount
```

Then append the Expense and Payment UI routes after your existing UI routes.

---

## Step 4: Create HTML Templates

Add the following new templates under `src/templates/masters`:

- `expense_list.html`
- `expense_form.html`
- `expense_detail.html`
- `payment_list.html`
- `payment_form.html`
- `payment_detail.html`

Also update `base.html` to add navigation links for Expenses and Payments.

---

## Step 5: Add CSS for Status

Update `src/static/css/style.css` with new status badge colors:

```css
.status-reconciled { background-color: #3498db; color: white; }
.status-paid { background-color: #2ecc71; color: white; }
.status-failed { background-color: #e74c3c; color: white; }
```

---

## Step 6: Seed Test Data

Create `scripts/seed_test_expense_payment.py` to seed sample Expense and Payment records.

---

## Step 7: Test and Validate

1. Run `uvicorn src.main:app --reload`
2. Open `http://localhost:8000/masters/expenses`
3. Create, view, update, delete expenses and payments
4. Verify reconciliation and recurring expense generation

---

## Acceptance Criteria

- Expenses and Payments have full CRUD in UI and API.
- Recurring expense templates can generate actual expense records.
- UTR numbers are unique.
- Payment reconciliation state works.
- Soft delete only sets `is_active = False`.

---

**Note:** This implementation assumes your DB models have the fields described in the API and UI layers. Adapt field names if your schema differs.
