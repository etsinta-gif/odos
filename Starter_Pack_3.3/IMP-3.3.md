# IMP-3.3 – Data Validation & Quality

**Document ID:** IMP-3.3  
**Version:** 1.0  
**Status:** Draft  
**Owner:** Aniket  
**Sprint:** 3.3  
**Phase:** Phase 3 – Canonical ETL Engine  
**Estimated Duration:** 2–3 days

---

## Sprint Overview

**Goal:** Validate transformed data against business rules (`RUL_ValidationRule`), detect duplicates, and log errors into `ETL_ErrorLog`.

---

## Prerequisites

- [ ] Sprint 3.2 completed (transformed data available)
- [ ] `RUL_ValidationRule` table exists and has at least one rule (e.g., "PAN must be 10 chars")
- [ ] `ETL_ErrorLog` model exists

---

## Task 3.3.1 – Validation Engine

**What:** Write a service that reads a list of transformed rows and applies all active validation rules for the company.

### Steps

1. **Create `src/etl/services/validator.py`:**

```python
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
```

2. **Test** with a sample row and a rule:

```python
from src.core.database import SessionLocal
db = SessionLocal()
row = {"PAN": "ABC123", "LoanAmount": 150000}
errors = apply_validation_rules(db, 1, row)
print(errors)
```

---

## Task 3.3.2 – Duplicate Detection

**What:** Detect duplicate records based on a configurable set of key fields (e.g., PAN, case number).

### Steps

1. **Create `src/etl/services/duplicate_detector.py`:**

```python
# src/etl/services/duplicate_detector.py
from sqlalchemy.orm import Session
from src.transactions.models import TRN_Case  # example target table

def check_duplicates(db: Session, company_id: int, row: dict, key_fields: list) -> bool:
    """Return True if a record with same key_fields exists in target table."""
    query = db.query(TRN_Case).filter(TRN_Case.company_id == company_id)
    for field in key_fields:
        value = row.get(field)
        if value is not None:
            query = query.filter(getattr(TRN_Case, field) == value)
    return query.first() is not None
```

2. **Integrate** into the validation step: for each row, check duplicates and log a warning if found.

---

## Task 3.3.3 – Error Logging

**What:** Store validation and duplicate errors into `ETL_ErrorLog`.

### Steps

1. **Ensure `ETL_ErrorLog` model is defined** (from Sprint 1.5) with columns: `error_log_id`, `batch_guid`, `company_id`, `table_name`, `row_number`, `column_name`, `error_type`, `error_message`, `error_datetime`.

2. **Modify the validation process** to insert errors:

```python
def log_errors(db: Session, batch_guid: str, company_id: int, row_index: int, errors: list):
    for err in errors:
        log = ETL_ErrorLog(
            batch_guid=batch_guid,
            company_id=company_id,
            table_name="staging",
            row_number=row_index,
            column_name="unknown",
            error_type="validation",
            error_message=err,
            error_datetime=datetime.utcnow()
        )
        db.add(log)
    db.commit()
```
```

---

## Acceptance Criteria

- [ ] Validation rules are applied to each row.
- [ ] Errors are logged to `ETL_ErrorLog`.
- [ ] Duplicate detection works (finds existing records).
- [ ] A row with multiple violations generates multiple error entries.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No validation rules found | Seed some rules in `RUL_ValidationRule` via script or SQL. |
| Duplicate detection always false | Ensure key_fields match actual table columns. |
| Error log not populated | Check that you commit the session after adding logs. |
