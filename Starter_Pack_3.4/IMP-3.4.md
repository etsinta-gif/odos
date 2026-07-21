# IMP-3.4 – Data Loading & Lineage

**Document ID:** IMP-3.4  
**Version:** 1.0  
**Status:** Draft  
**Owner:** Aniket  
**Sprint:** 3.4  
**Phase:** Phase 3 – Canonical ETL Engine  
**Estimated Duration:** 2–3 days

---

## Sprint Overview

**Goal:** Load validated data into production tables (`MST_`, `TRN_`) and record data lineage (`ETL_DataLineage`) to trace each record back to its source.

---

## Prerequisites

- [ ] Sprints 3.1–3.3 completed
- [ ] Transformed and validated data ready
- [ ] Target tables (`MST_Customer`, `TRN_Case`, etc.) already exist (from Phase 1)

---

## Task 3.4.1 – Loader Service

**What:** Insert rows into appropriate master/transaction tables.

### Steps

1. **Create `src/etl/services/loader.py`:**

```python
# src/etl/services/loader.py
from sqlalchemy.orm import Session
from src.masters.models import MST_Customer, MST_Company
from src.transactions.models import TRN_Case
from src.core.database import Base

def load_data(db: Session, company_id: int, rows: list, target_table: str) -> int:
    """
    Insert rows into the specified target table.
    Returns number of rows inserted.
    """
    model_map = {
        "MST_Customer": MST_Customer,
        "TRN_Case": TRN_Case,
    }
    model = model_map.get(target_table)
    if not model:
        raise ValueError(f"Unknown target table: {target_table}")
    inserted = 0
    for row in rows:
        row["company_id"] = company_id
        new_record = model(**row)
        db.add(new_record)
        inserted += 1
    db.commit()
    return inserted
```

2. **Integrate into ETL pipeline** – after validation, call this to load.

---

## Task 3.4.2 – Lineage Capture

**What:** For each inserted record, store lineage information in `ETL_DataLineage`.

### Steps

1. **Ensure `ETL_DataLineage` model exists** (from Sprint 1.5) with fields: `lineage_id`, `batch_guid`, `company_id`, `source_system`, `source_file`, `source_row`, `target_table`, `target_record_id`, `transformation_log`, `created_at`.

2. **Create `src/etl/services/lineage.py`:**

```python
# src/etl/services/lineage.py
from sqlalchemy.orm import Session
from src.etl.models import ETL_DataLineage
from datetime import datetime

def capture_lineage(db: Session, batch_guid: str, company_id: int, source_system: str,
                    source_file: str, source_row: int, target_table: str, target_record_id: int):
    lineage = ETL_DataLineage(
        batch_guid=batch_guid,
        company_id=company_id,
        source_system=source_system,
        source_file=source_file,
        source_row=source_row,
        target_table=target_table,
        target_record_id=target_record_id,
        transformation_log="mapped and validated",
        created_at=datetime.utcnow()
    )
    db.add(lineage)
    db.commit()
```

3. **Call this after each insert** to record lineage.

---

## Task 3.4.3 – Promote Script/API

**What:** Expose a final API endpoint that triggers the full ETL process: extract → transform → validate → load → lineage.

### Steps

1. **Create an endpoint** `POST /api/v1/etl/promote` that:
   - Accepts `batch_guid` and `target_table`.
   - Reads staging data for that batch.
   - Applies mapping, transformation, validation.
   - Loads valid rows into target table.
   - Captures lineage.

2. **Implement in `src/etl/api/etl.py`** (add to the existing router):

```python
@router.post("/promote")
def promote_batch(batch_guid: str, target_table: str, db: Session = Depends(get_db)):
    # Fetch staging rows
    # ... (use earlier services)
    return {"message": f"Promoted {inserted} rows to {target_table}"}
```
```

---

## Acceptance Criteria

- [ ] Data is inserted into the correct target tables.
- [ ] Each inserted record has a corresponding lineage entry.
- [ ] The promote API returns success with row count.
- [ ] Duplicate records are not inserted (if unique constraints exist).

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Foreign key violation | Ensure referenced records (e.g., company) exist. |
| Target table not found | Add the model to `model_map` in loader. |
| Lineage missing | Check that you commit after adding lineage records. |
| API returns 500 | Check the error logs; may be due to missing fields. |
