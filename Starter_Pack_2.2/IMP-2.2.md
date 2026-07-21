# IMP-2.2 – AI Mapping Suggestions

**Document ID:** IMP-2.2  
**Version:** 1.0  
**Status:** Draft  
**Owner:** Aniket  
**Sprint:** 2.2  
**Phase:** Phase 2 – AI Mapping Engine  
**Estimated Duration:** 2–3 days

---

## Sprint Overview

**Goal:** Build an AI‑powered service that suggests mappings between source columns (from `AI_Metadata`) and canonical fields (`META_FieldDefinition`), and expose it via a REST API.

---

## Prerequisites

- [ ] Phase 1 completed (Sprints 1.1–1.5)
- [ ] Sprint 2.1 completed (AI_Metadata table populated with at least one file)
- [ ] `META_FieldDefinition` seeded with core fields (e.g., `Customer Name`, `PAN`, `Disbursement Amount`, etc.)
- [ ] Docker containers running

---

## Task 2.2.1 – Mapping Suggester Service

**What:** Write a service that takes a list of source column names (from a file) and returns a list of suggested `META_FieldDefinition` matches with confidence scores.

### Steps

1. **Open VS Code** and open the `odos` folder.

2. **Open the terminal** (`` Ctrl+` ``).

3. **Create the service file** – `src/ai/services/mapping_suggester.py` and paste:

```python
# src/ai/services/mapping_suggester.py
import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.metadata.models import META_FieldDefinition
from src.ai.models import AI_Metadata

def suggest_mappings(db: Session, company_id: int, source_columns: List[str]) -> List[Dict[str, Any]]:
    """
    For each source column, suggest a target field from META_FieldDefinition.
    Returns a list of dicts with 'source_column', 'target_field', 'confidence'.
    """
    # Fetch all active field definitions for the company
    fields = db.query(META_FieldDefinition).filter(
        META_FieldDefinition.company_id == company_id,
        META_FieldDefinition.is_active == True
    ).all()
    
    suggestions = []
    for col in source_columns:
        best_match = None
        best_score = 0.0
        for field in fields:
            score = calculate_similarity(col, field.field_name, field.friendly_name, field.business_definition)
            if score > best_score:
                best_score = score
                best_match = field
        if best_match and best_score > 0.3:  # threshold
            suggestions.append({
                "source_column": col,
                "target_field_id": best_match.field_def_id,
                "target_field_name": best_match.field_name,
                "confidence": best_score
            })
    return suggestions

def calculate_similarity(source: str, field_name: str, friendly_name: str, business_def: str) -> float:
    """Simple heuristic: exact matches, partial matches, synonyms."""
    source_lower = source.lower()
    # Exact match on field name or friendly name
    if source_lower == field_name.lower() or source_lower == friendly_name.lower():
        return 1.0
    # Check if source is contained in friendly name or definition
    if source_lower in friendly_name.lower() or source_lower in business_def.lower():
        return 0.8
    # Check for common synonyms (simple mapping)
    synonyms = {
        "customer": ["borrower", "client", "applicant"],
        "pan": ["permanent account number", "pan card"],
        "amount": ["loan amount", "disbursement", "principal"],
        "date": ["dt", "date of", "timestamp"],
    }
    for key, syns in synonyms.items():
        if key in source_lower:
            for syn in syns:
                if syn in field_name.lower() or syn in friendly_name.lower():
                    return 0.7
    # Fallback: token overlap
    source_tokens = set(re.findall(r'\w+', source_lower))
    target_tokens = set(re.findall(r'\w+', field_name.lower() + " " + friendly_name.lower()))
    overlap = len(source_tokens & target_tokens)
    union = len(source_tokens | target_tokens)
    if union > 0:
        return overlap / union
    return 0.0
```

4. **Create a validator** to check if the suggested mapping is acceptable (e.g., confidence threshold).  
   - File: `src/ai/services/mapping_validator.py`

```python
# src/ai/services/mapping_validator.py
def validate_mapping_suggestion(suggestion: dict, min_confidence: float = 0.5) -> bool:
    """Return True if suggestion confidence is above threshold."""
    return suggestion.get("confidence", 0.0) >= min_confidence
```

5. **Test the suggester** manually in a Python shell:

```python
from src.core.database import SessionLocal
from src.ai.services.mapping_suggester import suggest_mappings
db = SessionLocal()
suggestions = suggest_mappings(db, company_id=1, source_columns=["Customer PAN", "Loan Amount", "Disbursement Date"])
print(suggestions)
db.close()
```

Expected output: a list of dictionaries with suggestions.

---

## Task 2.2.2 – API Endpoint

**What:** Expose the mapping suggestion logic as a REST API endpoint.

### Steps

1. **Create the API file** – `src/ai/api/mapping.py` and paste:

```python
# src/ai/api/mapping.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.ai.services.mapping_suggester import suggest_mappings
from src.ai.services.mapping_validator import validate_mapping_suggestion
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/ai/mapping", tags=["AI"])

class MappingRequest(BaseModel):
    source_columns: List[str]
    company_id: int
    min_confidence: float = 0.5

class MappingResponse(BaseModel):
    source_column: str
    target_field_id: int
    target_field_name: str
    confidence: float
    is_valid: bool

@router.post("/suggest", response_model=List[MappingResponse])
def suggest_mappings_endpoint(request: MappingRequest, db: Session = Depends(get_db)):
    # Fetch suggestions
    suggestions = suggest_mappings(db, request.company_id, request.source_columns)
    # Validate each and add to response
    result = []
    for s in suggestions:
        valid = validate_mapping_suggestion(s, request.min_confidence)
        result.append({
            "source_column": s["source_column"],
            "target_field_id": s["target_field_id"],
            "target_field_name": s["target_field_name"],
            "confidence": s["confidence"],
            "is_valid": valid
        })
    return result
```

2. **Register the router** in the main app (if not already).  
   - Open `src/main.py` (or the file where you mount routers) and add:

```python
from src.ai.api import mapping
app.include_router(mapping.router)
```

3. **Test the API** using curl or Postman:
   - Start the server: `uvicorn src.main:app --reload`
   - Send a POST request to `http://localhost:8000/ai/mapping/suggest` with JSON body:

```json
{
  "source_columns": ["Customer PAN", "Loan Amount", "Disbursement Date"],
  "company_id": 1
}
```

   - Expected response: array of mappings.

---

## Acceptance Criteria

- [ ] `suggest_mappings` returns at least one suggestion for known columns (e.g., "PAN" matches "PAN" field).
- [ ] Confidence scores are between 0 and 1.
- [ ] The API endpoint returns valid suggestions with `is_valid` flag.
- [ ] Suggestions with confidence below threshold are marked invalid.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `META_FieldDefinition` not found | Ensure you have seeded metadata (see Sprint 1.3). |
| No suggestions returned | Check that source column names are not empty; maybe adjust similarity logic. |
| API returns 500 | Check the server logs; ensure the router is imported. |
| `sqlalchemy.exc.NoSuchTableError` | Run migrations: `alembic upgrade head`. |
