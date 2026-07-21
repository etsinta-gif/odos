from datetime import date, datetime
import re
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.rules.models import RUL_CommissionRule, RUL_GSTRule, RUL_TDSRule, RUL_ValidationRule

router = APIRouter(prefix="/api/v1/rules", tags=["Rules"])


class ValidationRuleResponse(BaseModel):
    rule_id: int
    rule_code: str
    rule_name: str
    table_name: str
    field_name: str
    rule_type: str
    rule_expression: str
    severity: str
    is_active: bool
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class RuleExecutionRequest(BaseModel):
    table_name: str
    row_data: dict[str, Any]
    rule_ids: list[int] = []


class RuleExecutionResponse(BaseModel):
    passed: bool
    errors: list[str]
    warnings: list[str]


def _safe_eval_rule(expression: str, value: Any, row_data: dict[str, Any]) -> bool:
    allowed_globals = {"__builtins__": {}}
    allowed_locals = {
        "value": value,
        "row": row_data,
        "len": len,
        "re_match": lambda pattern, text: bool(re.match(pattern, str(text or ""))),
        "re_search": lambda pattern, text: bool(re.search(pattern, str(text or ""))),
        "is_none": lambda v: v is None,
        "is_not_none": lambda v: v is not None,
        "str": str,
        "int": int,
        "float": float,
    }
    return bool(eval(expression, allowed_globals, allowed_locals))


def execute_validation_rules(request: RuleExecutionRequest, db: Session) -> RuleExecutionResponse:
    errors: list[str] = []
    warnings: list[str] = []

    query = (
        db.query(RUL_ValidationRule)
        .filter(RUL_ValidationRule.table_name == request.table_name)
        .filter(RUL_ValidationRule.is_active == True)
        .order_by(RUL_ValidationRule.priority.asc(), RUL_ValidationRule.rule_id.asc())
    )
    if request.rule_ids:
        query = query.filter(RUL_ValidationRule.rule_id.in_(request.rule_ids))

    rules = query.all()

    for rule in rules:
        value = request.row_data.get(rule.field_name)
        try:
            passed = _safe_eval_rule(rule.rule_expression, value, request.row_data)
            if not passed:
                message = rule.error_message or f"Validation failed: {rule.rule_code}"
                if str(rule.severity).upper() in {"WARN", "WARNING"}:
                    warnings.append(message)
                else:
                    errors.append(message)
        except Exception as exc:
            errors.append(f"Rule execution error [{rule.rule_code}]: {exc}")

    return RuleExecutionResponse(passed=len(errors) == 0, errors=errors, warnings=warnings)


@router.get("/validation", response_model=list[ValidationRuleResponse])
def get_validation_rules(
    table_name: Optional[str] = None,
    is_active: bool = True,
    db: Session = Depends(get_db),
):
    query = db.query(RUL_ValidationRule).filter(RUL_ValidationRule.is_active == is_active)
    if table_name:
        query = query.filter(RUL_ValidationRule.table_name == table_name)
    return query.order_by(RUL_ValidationRule.priority.asc(), RUL_ValidationRule.rule_id.asc()).all()


@router.get("/validation/{rule_id}")
def get_validation_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(RUL_ValidationRule).filter(RUL_ValidationRule.rule_id == rule_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return rule


@router.post("/execute", response_model=RuleExecutionResponse)
def execute_rules(request: RuleExecutionRequest, db: Session = Depends(get_db)):
    return execute_validation_rules(request, db)


@router.post("/validation/bulk")
def bulk_load_validation_rules(payload: Any, force: bool = Query(False), db: Session = Depends(get_db)):
    if isinstance(payload, dict):
        rules = payload.get("validation_rules") or payload.get("rules") or []
    elif isinstance(payload, list):
        rules = payload
    else:
        rules = []

    loaded = 0
    for row in rules:
        code = row.get("RuleCode") or row.get("rule_code")
        if not code:
            continue

        existing = db.query(RUL_ValidationRule).filter(RUL_ValidationRule.rule_code == code).first()
        if existing and not force:
            continue

        model = existing or RUL_ValidationRule(rule_code=code)
        model.rule_name = row.get("RuleName") or row.get("rule_name") or code
        model.table_name = row.get("TableName") or row.get("table_name") or row.get("FieldScope") or "MST_Connector"
        model.field_name = row.get("FieldName") or row.get("field_name") or "pan"
        model.rule_type = row.get("ValidationType") or row.get("rule_type") or "EXPRESSION"
        model.rule_expression = row.get("ValidationExpression") or row.get("rule_expression") or "value is not None"
        model.severity = row.get("Severity") or row.get("severity") or "ERROR"
        model.error_message = row.get("ErrorMessage") or row.get("error_message")
        model.is_active = str(row.get("Status", "Active")).lower() != "inactive"
        model.priority = int(row.get("Priority") or row.get("priority") or 100)

        if not existing:
            db.add(model)
        loaded += 1

    db.commit()
    return {"loaded": loaded}


@router.post("/validation/test")
def test_validation_rules(payload: list[dict[str, Any]], db: Session = Depends(get_db)):
    results = []
    for idx, row in enumerate(payload):
        table_name = row.get("table_name", "MST_Connector")
        req = RuleExecutionRequest(table_name=table_name, row_data=row)
        out = execute_validation_rules(req, db)
        results.append({"record_id": idx + 1, "passed": out.passed, "errors": out.errors, "warnings": out.warnings})
    return {"results": results}


@router.get("/commission")
def get_commission_rules(
    lender_id: Optional[int] = None,
    product_id: Optional[int] = None,
    effective_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    query = db.query(RUL_CommissionRule).filter(RUL_CommissionRule.is_active == True)
    if lender_id is not None:
        query = query.filter(RUL_CommissionRule.lender_id == lender_id)
    if product_id is not None:
        query = query.filter(RUL_CommissionRule.product_id == product_id)
    if effective_date is not None:
        query = query.filter((RUL_CommissionRule.effective_from == None) | (RUL_CommissionRule.effective_from <= effective_date))
        query = query.filter((RUL_CommissionRule.effective_to == None) | (RUL_CommissionRule.effective_to >= effective_date))
    return query.all()


@router.post("/commission/bulk")
def bulk_load_commission_rules(payload: Any, force: bool = Query(False), db: Session = Depends(get_db)):
    rules = payload.get("commission_rules") if isinstance(payload, dict) else payload
    if not isinstance(rules, list):
        rules = []

    loaded = 0
    for row in rules:
        code = row.get("RuleCode") or row.get("rule_code")
        if not code:
            continue
        existing = db.query(RUL_CommissionRule).filter(RUL_CommissionRule.rule_code == code).first()
        if existing and not force:
            continue

        model = existing or RUL_CommissionRule(rule_code=code)
        model.rule_name = row.get("RuleName") or row.get("rule_name") or code
        model.lender_id = row.get("LenderID") or row.get("lender_id")
        model.product_id = row.get("ProductID") or row.get("product_id")
        model.basis_type = row.get("BasisType") or row.get("basis_type")
        model.calculation_type = row.get("CalculationType") or row.get("calculation_type") or "PERCENTAGE"
        model.flat_rate = row.get("FlatRate") or row.get("flat_rate")
        model.base_rate = row.get("BaseRate") or row.get("base_rate")
        model.connector_share = row.get("ConnectorShare") or row.get("connector_share")
        model.effective_rate = row.get("EffectiveRate") or row.get("effective_rate")
        model.status = row.get("Status") or row.get("status")
        model.is_active = str(model.status or "Active").lower() != "inactive"

        ef_from = row.get("EffectiveFrom") or row.get("effective_from")
        ef_to = row.get("EffectiveTo") or row.get("effective_to")
        if isinstance(ef_from, str):
            model.effective_from = datetime.fromisoformat(ef_from).date()
        if isinstance(ef_to, str):
            model.effective_to = datetime.fromisoformat(ef_to).date()

        if not existing:
            db.add(model)
        loaded += 1

    db.commit()
    return {"loaded": loaded}


@router.post("/tax/bulk")
def bulk_load_tax_rules(payload: Any, force: bool = Query(False), db: Session = Depends(get_db)):
    gst_rules = []
    tds_rules = []
    if isinstance(payload, dict):
        gst_rules = payload.get("gst_rules") or []
        tds_rules = payload.get("tds_rules") or []
    if isinstance(payload, list):
        for row in payload:
            code = str(row.get("RuleCode") or row.get("rule_code") or "")
            if code.upper().startswith("GST"):
                gst_rules.append(row)
            elif code.upper().startswith("TDS"):
                tds_rules.append(row)

    loaded_gst = 0
    for row in gst_rules:
        code = row.get("RuleCode") or row.get("rule_code")
        if not code:
            continue
        existing = db.query(RUL_GSTRule).filter(RUL_GSTRule.rule_code == code).first()
        if existing and not force:
            continue
        model = existing or RUL_GSTRule(rule_code=code)
        model.rule_name = row.get("RuleName") or row.get("rule_name") or code
        model.rate = float(row.get("Rate") or row.get("rate") or 0.0)
        model.applicability = row.get("Applicability") or row.get("applicability")
        model.reverse_charge = bool(row.get("ReverseCharge") or row.get("reverse_charge") or False)
        model.is_active = str(row.get("Status") or "Active").lower() != "inactive"
        if not existing:
            db.add(model)
        loaded_gst += 1

    loaded_tds = 0
    for row in tds_rules:
        code = row.get("RuleCode") or row.get("rule_code")
        if not code:
            continue
        existing = db.query(RUL_TDSRule).filter(RUL_TDSRule.rule_code == code).first()
        if existing and not force:
            continue
        model = existing or RUL_TDSRule(rule_code=code)
        model.rule_name = row.get("RuleName") or row.get("rule_name") or code
        model.section = row.get("Section") or row.get("section")
        model.rate = float(row.get("Rate") or row.get("rate") or 0.0)
        model.threshold = row.get("Threshold") or row.get("threshold")
        model.is_active = str(row.get("Status") or "Active").lower() != "inactive"
        if not existing:
            db.add(model)
        loaded_tds += 1

    db.commit()
    return {"loaded_gst": loaded_gst, "loaded_tds": loaded_tds}
