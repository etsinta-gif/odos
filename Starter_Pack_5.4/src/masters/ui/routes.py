from datetime import date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.masters.models import MST_Connector, MST_Customer, MST_Lender
from src.transactions.models import TRN_Case, TRN_Commission, TRN_Revenue

router = APIRouter(prefix="/masters", tags=["UI"])
TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


@router.get("/revenue")
async def revenue_list(
    request: Request,
    case_id: Optional[int] = None,
    payment_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TRN_Revenue).filter(TRN_Revenue.is_active == True)
    if case_id:
        query = query.filter(TRN_Revenue.case_id == case_id)
    if payment_status:
        query = query.filter(TRN_Revenue.payment_status == payment_status)
    revenues = query.all()
    for rev in revenues:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == rev.case_id).first()
        if case:
            rev.case_number = case.case_number
            lender = db.query(MST_Lender).filter(MST_Lender.lender_id == case.lender_id).first()
            rev.lender_name = lender.lender_name if lender else None
    return TEMPLATES.TemplateResponse(
        "masters/revenue_list.html",
        {"request": request, "revenues": revenues, "case_id": case_id, "payment_status": payment_status}
    )


@router.get("/revenue/add")
async def revenue_add_form(
    request: Request,
    case_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    cases_with_info = []
    for case in cases:
        customer = db.query(MST_Customer).filter(MST_Customer.customer_id == case.customer_id).first()
        cases_with_info.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "customer_name": customer.full_name if customer else "Unknown"
        })
    return TEMPLATES.TemplateResponse(
        "masters/revenue_form.html",
        {
            "request": request,
            "revenue": None,
            "action": "add",
            "cases": cases_with_info,
            "selected_case_id": case_id,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"]
        }
    )


@router.post("/revenue")
async def revenue_create(
    request: Request,
    case_id: int = Form(...),
    revenue_date: str = Form(...),
    base_revenue_amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    utr_number: Optional[str] = Form(None),
    payment_status: str = Form("PENDING"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.revenue import RevenueCreate, create_revenue

    revenue_data = RevenueCreate(
        case_id=case_id,
        revenue_date=date.fromisoformat(revenue_date),
        base_revenue_amount=base_revenue_amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        utr_number=utr_number,
        payment_status=payment_status,
        notes=notes
    )
    create_revenue(revenue_data, db)
    return RedirectResponse(url="/masters/revenue", status_code=303)


@router.get("/revenue/{revenue_id}")
async def revenue_detail(request: Request, revenue_id: int, db: Session = Depends(get_db)):
    rev = db.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revenue not found")
    case = db.query(TRN_Case).filter(TRN_Case.case_id == rev.case_id).first()
    lender = db.query(MST_Lender).filter(MST_Lender.lender_id == case.lender_id).first() if case else None
    return TEMPLATES.TemplateResponse(
        "masters/revenue_detail.html",
        {"request": request, "revenue": rev, "case": case, "lender": lender}
    )


@router.get("/revenue/{revenue_id}/edit")
async def revenue_edit_form(request: Request, revenue_id: int, db: Session = Depends(get_db)):
    rev = db.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
    if not rev:
        raise HTTPException(status_code=404, detail="Revenue not found")
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    cases_with_info = []
    for case in cases:
        customer = db.query(MST_Customer).filter(MST_Customer.customer_id == case.customer_id).first()
        cases_with_info.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "customer_name": customer.full_name if customer else "Unknown"
        })
    return TEMPLATES.TemplateResponse(
        "masters/revenue_form.html",
        {
            "request": request,
            "revenue": rev,
            "action": "edit",
            "cases": cases_with_info,
            "selected_case_id": rev.case_id,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"]
        }
    )


@router.post("/revenue/{revenue_id}/edit")
async def revenue_update(
    request: Request,
    revenue_id: int,
    case_id: int = Form(...),
    revenue_date: str = Form(...),
    base_revenue_amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    utr_number: Optional[str] = Form(None),
    payment_status: str = Form("PENDING"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.revenue import RevenueUpdate, update_revenue

    revenue_data = RevenueUpdate(
        revenue_date=date.fromisoformat(revenue_date),
        base_revenue_amount=base_revenue_amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        utr_number=utr_number,
        payment_status=payment_status,
        notes=notes
    )
    update_revenue(revenue_id, revenue_data, db)
    return RedirectResponse(url="/masters/revenue", status_code=303)


@router.get("/revenue/{revenue_id}/delete")
async def revenue_delete(revenue_id: int, db: Session = Depends(get_db)):
    from src.masters.api.revenue import delete_revenue

    delete_revenue(revenue_id, db)
    return RedirectResponse(url="/masters/revenue", status_code=303)


@router.get("/revenue/calculate/{case_id}")
async def revenue_calculate(case_id: int, db: Session = Depends(get_db)):
    from src.masters.api.revenue import calculate_revenue

    result = calculate_revenue(case_id, db)
    return RedirectResponse(
        url=(
            f"/masters/revenue/add?case_id={case_id}"
            f"&base_amount={result['base_revenue']}"
            f"&gst_amount={result['gst_amount']}"
            f"&tds_amount={result['tds_amount']}"
            f"&net_amount={result['net_amount']}"
        ),
        status_code=303
    )


@router.get("/commission")
async def commission_list(
    request: Request,
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
    commissions = query.all()
    for comm in commissions:
        case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id).first()
        if case:
            comm.case_number = case.case_number
        connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id).first()
        if connector:
            comm.connector_name = connector.full_name
    connectors = db.query(MST_Connector).filter(MST_Connector.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/commission_list.html",
        {
            "request": request,
            "commissions": commissions,
            "connectors": connectors,
            "case_id": case_id,
            "connector_id": connector_id,
            "payment_status": payment_status
        }
    )


@router.get("/commission/add")
async def commission_add_form(
    request: Request,
    case_id: Optional[int] = None,
    connector_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    cases_with_info = []
    for case in cases:
        customer = db.query(MST_Customer).filter(MST_Customer.customer_id == case.customer_id).first()
        cases_with_info.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "customer_name": customer.full_name if customer else "Unknown"
        })
    connectors = db.query(MST_Connector).filter(MST_Connector.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/commission_form.html",
        {
            "request": request,
            "commission": None,
            "action": "add",
            "cases": cases_with_info,
            "connectors": connectors,
            "selected_case_id": case_id,
            "selected_connector_id": connector_id,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"]
        }
    )


@router.post("/commission")
async def commission_create(
    request: Request,
    case_id: int = Form(...),
    connector_id: int = Form(...),
    commission_date: str = Form(...),
    base_commission_amount: float = Form(...),
    bonus_commission_amount: float = Form(0.0),
    gross_commission_amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    payment_status: str = Form("PENDING"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.commission import CommissionCreate, create_commission

    commission_data = CommissionCreate(
        case_id=case_id,
        connector_id=connector_id,
        commission_date=date.fromisoformat(commission_date),
        base_commission_amount=base_commission_amount,
        bonus_commission_amount=bonus_commission_amount,
        gross_commission_amount=gross_commission_amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        payment_status=payment_status,
        notes=notes
    )
    create_commission(commission_data, db)
    return RedirectResponse(url="/masters/commission", status_code=303)


@router.get("/commission/{commission_id}")
async def commission_detail(request: Request, commission_id: int, db: Session = Depends(get_db)):
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    case = db.query(TRN_Case).filter(TRN_Case.case_id == comm.case_id).first()
    connector = db.query(MST_Connector).filter(MST_Connector.connector_id == comm.connector_id).first()
    return TEMPLATES.TemplateResponse(
        "masters/commission_detail.html",
        {"request": request, "commission": comm, "case": case, "connector": connector}
    )


@router.get("/commission/{commission_id}/edit")
async def commission_edit_form(request: Request, commission_id: int, db: Session = Depends(get_db)):
    comm = db.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="Commission not found")
    cases = db.query(TRN_Case).filter(TRN_Case.is_active == True).all()
    cases_with_info = []
    for case in cases:
        customer = db.query(MST_Customer).filter(MST_Customer.customer_id == case.customer_id).first()
        cases_with_info.append({
            "case_id": case.case_id,
            "case_number": case.case_number,
            "customer_name": customer.full_name if customer else "Unknown"
        })
    connectors = db.query(MST_Connector).filter(MST_Connector.is_active == True).all()
    return TEMPLATES.TemplateResponse(
        "masters/commission_form.html",
        {
            "request": request,
            "commission": comm,
            "action": "edit",
            "cases": cases_with_info,
            "connectors": connectors,
            "selected_case_id": comm.case_id,
            "selected_connector_id": comm.connector_id,
            "payment_statuses": ["PENDING", "PAID", "FAILED", "RECONCILED"]
        }
    )


@router.post("/commission/{commission_id}/edit")
async def commission_update(
    request: Request,
    commission_id: int,
    case_id: int = Form(...),
    connector_id: int = Form(...),
    commission_date: str = Form(...),
    base_commission_amount: float = Form(...),
    bonus_commission_amount: float = Form(0.0),
    gross_commission_amount: float = Form(...),
    gst_amount: float = Form(0.0),
    tds_amount: float = Form(0.0),
    net_amount: float = Form(...),
    payment_status: str = Form("PENDING"),
    notes: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    from src.masters.api.commission import CommissionUpdate, update_commission

    commission_data = CommissionUpdate(
        case_id=case_id,
        connector_id=connector_id,
        commission_date=date.fromisoformat(commission_date),
        base_commission_amount=base_commission_amount,
        bonus_commission_amount=bonus_commission_amount,
        gross_commission_amount=gross_commission_amount,
        gst_amount=gst_amount,
        tds_amount=tds_amount,
        net_amount=net_amount,
        payment_status=payment_status,
        notes=notes
    )
    update_commission(commission_id, commission_data, db)
    return RedirectResponse(url="/masters/commission", status_code=303)


@router.get("/commission/{commission_id}/delete")
async def commission_delete(commission_id: int, db: Session = Depends(get_db)):
    from src.masters.api.commission import delete_commission

    delete_commission(commission_id, db)
    return RedirectResponse(url="/masters/commission", status_code=303)


@router.get("/commission/calculate/{case_id}")
async def commission_calculate(case_id: int, db: Session = Depends(get_db)):
    from src.masters.api.commission import calculate_commission

    result = calculate_commission(case_id, db)
    if "error" in result:
        return RedirectResponse(
            url=f"/masters/commission/add?case_id={case_id}&error={result['error']}",
            status_code=303
        )
    return RedirectResponse(
        url=(
            f"/masters/commission/add?case_id={case_id}"
            f"&base_commission={result['base_commission']}"
            f"&gst_amount={result['gst_amount']}"
            f"&tds_amount={result['tds_amount']}"
            f"&net_amount={result['net_amount']}"
        ),
        status_code=303
    )
