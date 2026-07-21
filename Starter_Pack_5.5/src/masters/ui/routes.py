from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.masters.api.expense import ExpenseCreate, ExpenseUpdate, create_expense, update_expense, delete_expense
from src.masters.api.payment import PaymentCreate, PaymentUpdate, create_payment, update_payment, delete_payment, reconcile_payment
from src.masters.models import MST_Vendor, MST_ExpenseCategory, MST_CostCenter, MST_CompanyBankAccount
from src.transactions.models import TRN_Expense, TRN_Payment, TRN_Case

router = APIRouter(prefix="/masters", tags=["UI"])
TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


@router.get("/expenses")
async def expense_list(
    request: Request,
    vendor_id: Optional[int] = None,
    expense_category_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Expense).filter(TRN_Expense.is_active == True)
    if vendor_id:
        query = query.filter(TRN_Expense.vendor_id == vendor_id)
    if expense_category_id:
        query = query.filter(TRN_Expense.expense_category_id == expense_category_id)
    if payment_status:
        query = query.filter(TRN_Expense.payment_status == payment_status)
    expenses = query.all()

    for expense in expenses:
        vendor = db.query(MST_Vendor).filter(MST_Vendor.vendor_id == expense.vendor_id).first()
        expense.vendor_name = vendor.vendor_name if vendor else None
        category = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.expense_category_id == expense.expense_category_id).first()
        expense.expense_category_name = category.category_name if category else None
        cost_center = db.query(MST_CostCenter).filter(MST_CostCenter.cost_center_id == expense.cost_center_id).first()
        expense.cost_center_name = cost_center.center_name if cost_center else None
        case = db.query(TRN_Case).filter(TRN_Case.case_id == expense.case_id).first()
        expense.case_number = case.case_number if case else None

    vendors = db.query(MST_Vendor).filter(MST_Vendor.is_active == True).all()
    categories = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/expense_list.html",
        {
            "request": request,
            "expenses": expenses,
            "vendors": vendors,
            "categories": categories,
            "vendor_id": vendor_id,
            "expense_category_id": expense_category_id,
            "payment_status": payment_status,
        }
    )


@router.get("/expenses/add")
async def expense_add_form(request: Request, db: Session = Depends(get_db)):
    vendors = db.query(MST_Vendor).filter(MST_Vendor.is_active == True).all()
    categories = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.is_active == True).all()
    cost_centers = db.query(MST_CostCenter).filter(MST_CostCenter.is_active == True).all()
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/expense_form.html",
        {
            "request": request,
            "expense": None,
            "action": "add",
            "vendors": vendors,
            "categories": categories,
            "cost_centers": cost_centers,
            "cases": cases,
            "selected_vendor_id": None,
            "selected_category_id": None,
            "selected_cost_center_id": None,
            "selected_case_id": None,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"],
        }
    )


@router.post("/expenses")
async def expense_create(
    request: Request,
    expense_date: str = Form(...),
    vendor_id: Optional[int] = Form(None),
    expense_category_id: int = Form(...),
    cost_center_id: Optional[int] = Form(None),
    case_id: Optional[int] = Form(None),
    description: str = Form(...),
    amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    payment_status: str = Form("PENDING"),
    invoice_reference: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    expense_data = ExpenseCreate(
        expense_date=date.fromisoformat(expense_date),
        vendor_id=vendor_id,
        expense_category_id=expense_category_id,
        cost_center_id=cost_center_id,
        case_id=case_id,
        description=description,
        amount=amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        payment_status=payment_status,
        invoice_reference=invoice_reference,
        notes=notes,
    )
    create_expense(expense_data, db)
    return RedirectResponse(url="/masters/expenses", status_code=303)


@router.get("/expenses/{expense_id}")
async def expense_detail(request: Request, expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(TRN_Expense).filter(TRN_Expense.expense_id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    vendor = db.query(MST_Vendor).filter(MST_Vendor.vendor_id == expense.vendor_id).first()
    category = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.expense_category_id == expense.expense_category_id).first()
    cost_center = db.query(MST_CostCenter).filter(MST_CostCenter.cost_center_id == expense.cost_center_id).first()
    case = db.query(TRN_Case).filter(TRN_Case.case_id == expense.case_id).first()

    return TEMPLATES.TemplateResponse(
        "masters/expense_detail.html",
        {
            "request": request,
            "expense": expense,
            "vendor": vendor,
            "category": category,
            "cost_center": cost_center,
            "case": case,
        }
    )


@router.get("/expenses/{expense_id}/edit")
async def expense_edit_form(request: Request, expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(TRN_Expense).filter(TRN_Expense.expense_id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    vendors = db.query(MST_Vendor).filter(MST_Vendor.is_active == True).all()
    categories = db.query(MST_ExpenseCategory).filter(MST_ExpenseCategory.is_active == True).all()
    cost_centers = db.query(MST_CostCenter).filter(MST_CostCenter.is_active == True).all()
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()

    return TEMPLATES.TemplateResponse(
        "masters/expense_form.html",
        {
            "request": request,
            "expense": expense,
            "action": "edit",
            "vendors": vendors,
            "categories": categories,
            "cost_centers": cost_centers,
            "cases": cases,
            "selected_vendor_id": expense.vendor_id,
            "selected_category_id": expense.expense_category_id,
            "selected_cost_center_id": expense.cost_center_id,
            "selected_case_id": expense.case_id,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"],
        }
    )


@router.post("/expenses/{expense_id}/edit")
async def expense_update(
    request: Request,
    expense_id: int,
    expense_date: str = Form(...),
    vendor_id: Optional[int] = Form(None),
    expense_category_id: int = Form(...),
    cost_center_id: Optional[int] = Form(None),
    case_id: Optional[int] = Form(None),
    description: str = Form(...),
    amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    payment_status: str = Form("PENDING"),
    invoice_reference: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(True),
    db: Session = Depends(get_db),
):
    expense_data = ExpenseUpdate(
        expense_date=date.fromisoformat(expense_date),
        vendor_id=vendor_id,
        expense_category_id=expense_category_id,
        cost_center_id=cost_center_id,
        case_id=case_id,
        description=description,
        amount=amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        payment_status=payment_status,
        invoice_reference=invoice_reference,
        notes=notes,
        is_active=is_active,
    )
    update_expense(expense_id, expense_data, db)
    return RedirectResponse(url="/masters/expenses", status_code=303)


@router.get("/expenses/{expense_id}/delete")
async def expense_delete_route(expense_id: int, db: Session = Depends(get_db)):
    delete_expense(expense_id, db)
    return RedirectResponse(url="/masters/expenses", status_code=303)


@router.get("/payments")
async def payment_list(
    request: Request,
    payment_type: Optional[str] = None,
    reconciliation_status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(TRN_Payment).filter(TRN_Payment.is_active == True)
    if payment_type:
        query = query.filter(TRN_Payment.payment_type == payment_type)
    if reconciliation_status:
        query = query.filter(TRN_Payment.reconciliation_status == reconciliation_status)
    payments = query.all()

    for payment in payments:
        bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id).first()
        payment.bank_name = bank.bank_name if bank else None
    banks = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/payment_list.html",
        {
            "request": request,
            "payments": payments,
            "banks": banks,
            "payment_type": payment_type,
            "reconciliation_status": reconciliation_status,
        }
    )


@router.get("/payments/add")
async def payment_add_form(request: Request, db: Session = Depends(get_db)):
    banks = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/payment_form.html",
        {
            "request": request,
            "payment": None,
            "action": "add",
            "banks": banks,
            "payment_types": ["EXPENSE", "COMMISSION", "SALARY", "VENDOR"],
            "reconciliation_statuses": ["PENDING", "RECONCILED", "FAILED"],
        }
    )


@router.post("/payments")
async def payment_create(
    request: Request,
    payment_date: str = Form(...),
    company_bank_account_id: int = Form(...),
    payment_amount: float = Form(...),
    payment_mode: str = Form(...),
    utr_number: Optional[str] = Form(None),
    payment_type: str = Form(...),
    reference_id: int = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    payment_data = PaymentCreate(
        payment_date=date.fromisoformat(payment_date),
        company_bank_account_id=company_bank_account_id,
        payment_amount=payment_amount,
        payment_mode=payment_mode,
        utr_number=utr_number,
        payment_type=payment_type,
        reference_id=reference_id,
        notes=notes,
    )
    create_payment(payment_data, db)
    return RedirectResponse(url="/masters/payments", status_code=303)


@router.get("/payments/{payment_id}")
async def payment_detail(request: Request, payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    bank = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.bank_account_id == payment.company_bank_account_id).first()
    return TEMPLATES.TemplateResponse(
        "masters/payment_detail.html",
        {"request": request, "payment": payment, "bank": bank}
    )


@router.get("/payments/{payment_id}/edit")
async def payment_edit_form(request: Request, payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(TRN_Payment).filter(TRN_Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    banks = db.query(MST_CompanyBankAccount).filter(MST_CompanyBankAccount.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/payment_form.html",
        {
            "request": request,
            "payment": payment,
            "action": "edit",
            "banks": banks,
            "payment_types": ["EXPENSE", "COMMISSION", "SALARY", "VENDOR"],
            "reconciliation_statuses": ["PENDING", "RECONCILED", "FAILED"],
        }
    )


@router.post("/payments/{payment_id}/edit")
async def payment_update(
    request: Request,
    payment_id: int,
    payment_date: str = Form(...),
    company_bank_account_id: int = Form(...),
    payment_amount: float = Form(...),
    payment_mode: str = Form(...),
    utr_number: Optional[str] = Form(None),
    payment_type: str = Form(...),
    reference_id: int = Form(...),
    reconciliation_status: str = Form("PENDING"),
    notes: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(True),
    db: Session = Depends(get_db),
):
    payment_data = PaymentUpdate(
        payment_date=date.fromisoformat(payment_date),
        company_bank_account_id=company_bank_account_id,
        payment_amount=payment_amount,
        payment_mode=payment_mode,
        utr_number=utr_number,
        payment_type=payment_type,
        reference_id=reference_id,
        reconciliation_status=reconciliation_status,
        notes=notes,
        is_active=is_active,
    )
    update_payment(payment_id, payment_data, db)
    return RedirectResponse(url="/masters/payments", status_code=303)


@router.get("/payments/{payment_id}/delete")
async def payment_delete_route(payment_id: int, db: Session = Depends(get_db)):
    delete_payment(payment_id, db)
    return RedirectResponse(url="/masters/payments", status_code=303)


@router.get("/payments/{payment_id}/reconcile")
async def payment_reconcile_route(payment_id: int, db: Session = Depends(get_db)):
    reconcile_payment(payment_id, db)
    return RedirectResponse(url="/masters/payments", status_code=303)
