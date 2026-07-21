# src/masters/ui/routes.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.masters.models import MST_Customer, MST_Lender, MST_Product
from src.masters.api.case import create_case, update_case, delete_case, transition_status, CaseCreate, CaseUpdate
from src.transactions.models import TRN_Case

router = APIRouter(prefix="/masters", tags=["UI"])
templates = Jinja2Templates(directory="src/templates")

CASE_STATUSES = ["LEAD", "APPLICATION", "SANCTIONED", "DISBURSED", "CLOSED"]

@router.get("/cases")
async def case_list(request: Request, db: Session = Depends(get_db)):
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    return templates.TemplateResponse(
        "masters/case_list.html",
        {"request": request, "cases": cases}
    )

@router.get("/cases/add")
async def case_add_form(request: Request, db: Session = Depends(get_db)):
    customers = db.query(MST_Customer).filter(MST_Customer.is_active == True).all()
    lenders = db.query(MST_Lender).filter(MST_Lender.is_active == True).all()
    products = db.query(MST_Product).filter(MST_Product.is_active == True).all()
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
    create_case(case_data, db)
    return RedirectResponse(url="/masters/cases", status_code=303)

@router.get("/cases/{case_id}")
async def case_detail(request: Request, case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return templates.TemplateResponse(
        "masters/case_detail.html",
        {"request": request, "case": case, "statuses": CASE_STATUSES}
    )

@router.get("/cases/{case_id}/edit")
async def case_edit_form(request: Request, case_id: int, db: Session = Depends(get_db)):
    case = db.query(TRN_Case).filter(TRN_Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    customers = db.query(MST_Customer).filter(MST_Customer.is_active == True).all()
    lenders = db.query(MST_Lender).filter(MST_Lender.is_active == True).all()
    products = db.query(MST_Product).filter(MST_Product.is_active == True).all()
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
    db: Session = Depends(get_db)
):
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
async def case_delete(case_id: int, db: Session = Depends(get_db)):
    delete_case(case_id, db)
    return RedirectResponse(url="/masters/cases", status_code=303)

@router.post("/cases/{case_id}/status")
async def case_transition_status(
    request: Request,
    case_id: int,
    new_status: str = Form(...),
    db: Session = Depends(get_db)
):
    transition_status(case_id, new_status, db)
    return RedirectResponse(url=f"/masters/cases/{case_id}", status_code=303)
