from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.rules.models import RUL_CommissionRule, RUL_GSTRule, RUL_TDSRule, RUL_ValidationRule
from src.security.auth import get_current_user
from src.transactions.models import RUL_CommissionSlab

router = APIRouter(prefix="/masters/rules", tags=["Rules UI"], dependencies=[Depends(get_current_user)])
TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


@router.get("/validation")
def validation_rules_list(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RUL_ValidationRule).order_by(RUL_ValidationRule.priority.asc(), RUL_ValidationRule.rule_id.asc()).all()
    return TEMPLATES.TemplateResponse("masters/rules_validation_list.html", {"request": request, "rows": rows})


@router.get("/commission")
def commission_rules_list(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RUL_CommissionRule).order_by(RUL_CommissionRule.commission_rule_id.desc()).all()
    return TEMPLATES.TemplateResponse("masters/rules_commission_list.html", {"request": request, "rows": rows})


@router.get("/commission-slabs")
def commission_slab_list(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RUL_CommissionSlab).order_by(RUL_CommissionSlab.slab_id.desc()).all()
    return TEMPLATES.TemplateResponse("masters/rules_commission_slab_list.html", {"request": request, "rows": rows})


@router.get("/gst")
def gst_rules_list(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RUL_GSTRule).order_by(RUL_GSTRule.gst_rule_id.desc()).all()
    return TEMPLATES.TemplateResponse("masters/rules_gst_list.html", {"request": request, "rows": rows})


@router.get("/tds")
def tds_rules_list(request: Request, db: Session = Depends(get_db)):
    rows = db.query(RUL_TDSRule).order_by(RUL_TDSRule.tds_rule_id.desc()).all()
    return TEMPLATES.TemplateResponse("masters/rules_tds_list.html", {"request": request, "rows": rows})
