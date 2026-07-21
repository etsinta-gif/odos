# src/etl/services/validator.py
from sqlalchemy.orm import Session
from src.rules.models import RUL_ValidationRule
import re

def apply_validation_rules(db: Session, company_id: int, row: dict) -> list:
    """Apply all active validation rules to a single transformed row.
       Returns a list of error messages (empty if passes)."""
    rules = db.query(RUL_ValidationRule).filter(
        RUL_ValidationRule.company_id == company_id,
        RUL_ValidationRule.is_active == True
    ).all()
    errors = []
    for rule in rules:
        field_value = row.get(rule.field_name)
        if rule.is_mandatory and (field_value is None or field_value == ""):
            errors.append(f"Mandatory field '{rule.field_name}' is missing.")
            continue
        if rule.regex_pattern and field_value:
            if not re.match(rule.regex_pattern, str(field_value)):
                errors.append(f"Field '{rule.field_name}' failed pattern: {rule.regex_pattern}")
        if rule.min_value is not None and field_value is not None:
            if isinstance(field_value, (int, float)) and field_value < rule.min_value:
                errors.append(f"Field '{rule.field_name}' below minimum {rule.min_value}")
        if rule.max_value is not None and field_value is not None:
            if isinstance(field_value, (int, float)) and field_value > rule.max_value:
                errors.append(f"Field '{rule.field_name}' above maximum {rule.max_value}")
    return errors
