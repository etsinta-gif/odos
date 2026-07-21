# IMP-3.2 – Data Transformation & Mapping

**Document ID:** IMP-3.2  
**Version:** 1.0  
**Status:** Draft  
**Owner:** Aniket  
**Sprint:** 3.2  
**Phase:** Phase 3 – Canonical ETL Engine  
**Estimated Duration:** 2–3 days

---

## Sprint Overview

**Goal:** Transform raw staging data (from `ETL_StagingRawData`) into structured records using confirmed mappings from `META_FieldMapping`, perform type conversions, and prepare the data for validation.

---

## Prerequisites

- [ ] Phase 1 and Sprint 3.1 completed
- [ ] At least one file has been uploaded and staged (data in `ETL_StagingRawData`)
- [ ] Some mappings exist in `META_FieldMapping` (can be manually inserted for testing)

---

## Task 3.2.1 – Mapper Service

**What:** Write a service that reads a raw row (dict of source columns → values) and applies the stored field mappings to produce a dict of canonical field names → values.

### Steps

1. **Create `src/etl/services/mapper.py`:**

```python
# src/etl/services/mapper.py
from sqlalchemy.orm import Session
from src.metadata.models import META_FieldMapping, META_FieldDefinition

def get_mappings(db: Session, company_id: int, source_system: str):
    """Fetch all active mappings for a given source system."""
    mappings = db.query(META_FieldMapping).filter(
        META_FieldMapping.company_id == company_id,
        META_FieldMapping.source_system == source_system,
        META_FieldMapping.is_verified == True
    ).all()
    mapping_dict = {}
    for m in mappings:
        target_field = db.query(META_FieldDefinition).filter_by(field_def_id=m.field_def_id).first()
        if target_field:
            mapping_dict[m.source_header] = target_field.field_name
    return mapping_dict


def apply_mapping(raw_row: dict, mapping_dict: dict) -> dict:
    """Transform a raw row using the mapping dict."""
    transformed = {}
    for source_col, value in raw_row.items():
        if source_col in mapping_dict:
            transformed[mapping_dict[source_col]] = value
    return transformed
```

2. **Test** in Python shell:

```python
from src.core.database import SessionLocal
db = SessionLocal()
mapping = get_mappings(db, company_id=1, source_system="HDFC")
raw = {"Customer Name": "John Doe", "Loan Amount": 150000}
transformed = apply_mapping(raw, mapping)
print(transformed)
```

---

## Task 3.2.2 – Type Conversion

**What:** Convert values to the correct data type based on the target field definition (e.g., `META_FieldDefinition.logical_data_type`).

### Steps

1. **Create `src/etl/services/transformer.py`** (which will use the mapper and then convert types):

```python
# src/etl/services/transformer.py
from sqlalchemy.orm import Session
from src.etl.services.mapper import get_mappings, apply_mapping
from src.metadata.models import META_FieldDefinition
from datetime import datetime
import re

def convert_type(value, logical_type: str):
    """Convert value to the appropriate Python type based on logical_type."""
    if value is None or value == "":
        return None
    logical_type = logical_type.lower()
    if "date" in logical_type:
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except (ValueError, TypeError):
                continue
        return None
    if "decimal" in logical_type or "amount" in logical_type or "numeric" in logical_type:
        cleaned = re.sub(r'[^\d.]', '', str(value))
        try:
            return float(cleaned)
        except ValueError:
            return None
    if "integer" in logical_type:
        try:
            return int(value)
        except ValueError:
            return None
    if "boolean" in logical_type:
        return str(value).lower() in ("yes", "true", "1", "y")
    return str(value)


def transform_raw_data(db: Session, company_id: int, source_system: str, raw_rows: list) -> list:
    """
    For each raw row, apply mapping and type conversion.
    Returns list of transformed dicts with canonical field names and converted values.
    """
    mappings = get_mappings(db, company_id, source_system)
    field_defs = db.query(META_FieldDefinition).filter(
        META_FieldDefinition.company_id == company_id
    ).all()
    field_type_map = {f.field_name: f.logical_data_type for f in field_defs}
    transformed_rows = []
    for raw in raw_rows:
        mapped = apply_mapping(raw, mappings)
        converted = {}
        for field, value in mapped.items():
            logical_type = field_type_map.get(field, "text")
            converted[field] = convert_type(value, logical_type)
        transformed_rows.append(converted)
    return transformed_rows
```

2. **Integrate into the ETL pipeline** by adding a method to `ETLPipeline`:

```python
def transform(self, raw_rows, source_system):
    return transform_raw_data(self.db, self.company_id, source_system, raw_rows)
```

---

## Acceptance Criteria

- [ ] Mapped rows contain only target field names.
- [ ] Date strings are converted to Python `date` objects.
- [ ] Numeric strings (with commas) are converted to `float` or `int`.
- [ ] Null/empty values are preserved as `None`.
- [ ] Transformation works on a sample raw row.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `META_FieldMapping` is empty | Manually insert a few test mappings using the API or SQL. |
| Date conversion fails | Check if the format is supported; add more patterns to `convert_type`. |
| Type conversion error | Ensure the logical_type is set correctly in `META_FieldDefinition`. |
| `source_system` mismatch | Use the correct source system name (e.g., from `AI_Metadata`). |
