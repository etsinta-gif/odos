# src/masters/ui/routes.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.masters.models import MST_Customer, MST_Lender, MST_Product
from src.masters.api.case import create_case, update_case, delete_case, transition_status, CaseCreate, CaseUpdate
from src.security.auth import get_current_user
from src.security.models import SEC_User
from src.transactions.models import TRN_Case

router = APIRouter(prefix="/masters", tags=["UI"], dependencies=[Depends(get_current_user)])
templates = Jinja2Templates(directory="src/templates")

CASE_STATUSES = ["LEAD", "APPLICATION", "SANCTIONED", "DISBURSED", "CLOSED"]


def _ensure_case_access(case: TRN_Case | None, company_id: int) -> TRN_Case:
    if not case or case.company_id != company_id:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.get("/cases")
async def case_list(
    request: Request,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cases = (
        db.query(TRN_Case)
        .filter(TRN_Case.company_id == current_user.company_id)
        .filter(TRN_Case.is_active == True)
        .all()
    )
    return templates.TemplateResponse(
        "masters/case_list.html",
        {"request": request, "cases": cases}
    )

@router.get("/cases/add")
async def case_add_form(
    request: Request,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    customers = db.query(MST_Customer).filter(MST_Customer.company_id == current_user.company_id).filter(MST_Customer.is_active == True).all()
    lenders = db.query(MST_Lender).filter(MST_Lender.company_id == current_user.company_id).filter(MST_Lender.is_active == True).all()
    products = db.query(MST_Product).filter(MST_Product.company_id == current_user.company_id).filter(MST_Product.is_active == True).all()
    return templates.TemplateResponse(
        "masters/case_form.html",
        {
            "request": request,
            "case": None,
            "customers": customers,
            "lenders": lenders,
            "products": products,
            "statuses": CASE_STATUSES,
            "action": "add"
        }
    )

@router.post("/cases")
async def case_create(
    request: Request,
    customer_id: int = Form(...),
    lender_id: int = Form(...),
    product_id: int = Form(...),
    application_date: str = Form(None),
    sanction_date: str = Form(None),
    disbursement_date: str = Form(None),
    sanction_amount: float = Form(None),
    disbursement_amount: float = Form(None),
    case_number: str = Form(None),
    status: str = Form("LEAD"),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    case_data = CaseCreate(
        customer_id=customer_id,
        lender_id=lender_id,
        product_id=product_id,
        application_date=application_date,
        sanction_date=sanction_date,
        disbursement_date=disbursement_date,
        sanction_amount=sanction_amount,
        disbursement_amount=disbursement_amount,
        case_number=case_number,
        status=status
    )
    new_case = create_case(case_data, db)
    new_case.company_id = current_user.company_id
    db.add(new_case)
    db.commit()
    return RedirectResponse(url="/masters/cases", status_code=303)

@router.get("/cases/{case_id}")
async def case_detail(
    request: Request,
    case_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    case = _ensure_case_access(case, current_user.company_id)
    return templates.TemplateResponse(
        "masters/case_detail.html",
        {"request": request, "case": case, "statuses": CASE_STATUSES}
    )

@router.get("/cases/{case_id}/edit")
async def case_edit_form(
    request: Request,
    case_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    case = _ensure_case_access(case, current_user.company_id)
    customers = db.query(MST_Customer).filter(MST_Customer.company_id == current_user.company_id).filter(MST_Customer.is_active == True).all()
    lenders = db.query(MST_Lender).filter(MST_Lender.company_id == current_user.company_id).filter(MST_Lender.is_active == True).all()
    products = db.query(MST_Product).filter(MST_Product.company_id == current_user.company_id).filter(MST_Product.is_active == True).all()
    return templates.TemplateResponse(
        "masters/case_form.html",
        {
            "request": request,
            "case": case,
            "customers": customers,
            "lenders": lenders,
            "products": products,
            "statuses": CASE_STATUSES,
            "action": "edit"
        }
    )

@router.post("/cases/{case_id}/edit")
async def case_update(
    request: Request,
    case_id: int,
    customer_id: int = Form(...),
    lender_id: int = Form(...),
    product_id: int = Form(...),
    application_date: str = Form(None),
    sanction_date: str = Form(None),
    disbursement_date: str = Form(None),
    sanction_amount: float = Form(None),
    disbursement_amount: float = Form(None),
    case_number: str = Form(None),
    status: str = Form(None),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    _ensure_case_access(existing, current_user.company_id)
    case_data = CaseUpdate(
        customer_id=customer_id,
        lender_id=lender_id,
        product_id=product_id,
        application_date=application_date,
        sanction_date=sanction_date,
        disbursement_date=disbursement_date,
        sanction_amount=sanction_amount,
        disbursement_amount=disbursement_amount,
        status=status
    )
    update_case(case_id, case_data, db)
    return RedirectResponse(url=f"/masters/cases/{case_id}", status_code=303)

@router.get("/cases/{case_id}/delete")
async def case_delete(
    case_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    _ensure_case_access(existing, current_user.company_id)
    delete_case(case_id, db)
    return RedirectResponse(url="/masters/cases", status_code=303)

@router.post("/cases/{case_id}/status")
async def case_transition_status(
    request: Request,
    case_id: int,
    new_status: str = Form(...),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    _ensure_case_access(existing, current_user.company_id)
    transition_status(case_id, new_status, db)
    return RedirectResponse(url=f"/masters/cases/{case_id}", status_code=303)
