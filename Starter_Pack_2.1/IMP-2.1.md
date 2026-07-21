# IMP-2.1 – AI Metadata Learning

## Sprint Overview
**Goal:** Teach the system to recognise file structures, patterns, and source systems so that it can later suggest mappings automatically.

## Prerequisites (checklist):
- [ ] Phase 1 completed (Sprints 1.1–1.5)
- [ ] Repository is in `~/odos` (or your chosen folder)
- [ ] Docker containers are running (`docker-compose up -d`)
- [ ] You have a sample Excel file (e.g., a lender MIS) to test with

---

## Task 2.1.1 – File Fingerprinting

**What:** When a user uploads a file, we compute a SHA‑256 hash (fingerprint) and store it in the `AI_Metadata` table. This lets us detect duplicate uploads and recognise known files.

**Steps:**

1. **Open VS Code** and open the `odos` folder (File → Open Folder…).

2. **Open the terminal** (View → Terminal or press `` Ctrl+` ``).

3. **Activate your virtual environment** (if you are using one). If you used `uv`, run:
   ```
   > source .venv/bin/activate
   ```
   (On Windows: `.venv\Scripts\activate`)

4. **Create the AI models file** if it doesn't exist:
   - Open `src/ai/models.py`. If the folder/file doesn't exist, create it.
   - Paste the following code:

```python
# src/ai/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from src.core.database import Base

class AI_Metadata(Base):
    __tablename__ = "ai_metadata"
    metadata_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mst_company.company_id"), nullable=False)
    source_system = Column(String(100), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True)   # SHA-256
    sheet_name = Column(String(100), nullable=True)
    header_columns = Column(Text, nullable=True)                  # JSON list
    data_types = Column(Text, nullable=True)                      # JSON dict
    row_count = Column(Integer, nullable=True)
    import_batch_guid = Column(String(36), nullable=True)
    confidence = Column(Float, nullable=True)                     # overall confidence
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

5. **Create the migration** to add this table:
   ```
   > alembic revision --autogenerate -m "add_ai_metadata"
   ```
   - Expected output: `Generating .../versions/xxxx_add_ai_metadata.py`

6. **Apply the migration**:
   ```
   > alembic upgrade head
   ```
   - Expected output: `INFO  [alembic.runtime.migration] Running upgrade ...`

7. **Create a service** to compute the fingerprint:
   - Open `src/ai/services/fingerprint.py`
   - Paste:

```python
# src/ai/services/fingerprint.py
import hashlib

def compute_file_hash(file_bytes: bytes) -> str:
    """Return SHA-256 hex digest of file content."""
    return hashlib.sha256(file_bytes).hexdigest()
```

8. **Update the upload endpoint** (in `src/etl/api/etl.py`) to call this:
   - After receiving the file, read `file_bytes` and compute the hash.
   - Check if a record with that hash already exists; if yes, return a warning.
   - Store the hash in a new `AI_Metadata` record (along with other metadata).

**Expected output:** When you upload the same file twice, the second attempt returns a message like `"Duplicate file detected (same fingerprint)"`.

**Troubleshooting:**
- If `alembic` is not found, run `uv pip install alembic` first.
- If the database is not running, start Docker containers: `docker-compose up -d`.

---

## Task 2.1.2 – Pattern Recognition

**What:** We analyse the data in each column to detect common patterns (dates, amounts, PAN, GSTIN, etc.) and store these as metadata.

**Steps:**

1. **Create a pattern detection utility**:
   - Open `src/ai/services/pattern_detector.py` and paste:

```python
# src/ai/services/pattern_detector.py
import re
from typing import List, Dict, Any

def detect_patterns(column_values: List[str]) -> Dict[str, Any]:
    """Detect patterns like date, PAN, amount, percentage."""
    patterns = {}
    # Date pattern (YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, etc.)
    date_pattern = r'\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}'
    if any(re.search(date_pattern, str(v)) for v in column_values if v):
        patterns['is_date'] = True
    # PAN pattern (5 letters, 4 digits, 1 letter)
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    if any(re.search(pan_pattern, str(v)) for v in column_values if v):
        patterns['is_pan'] = True
    # Amount pattern (numbers with commas, decimals)
    amount_pattern = r'^\d{1,3}(,\d{3})*(\.\d{1,2})?$'
    if any(re.match(amount_pattern, str(v)) for v in column_values if v):
        patterns['is_amount'] = True
    # Percentage pattern (number followed by %)
    percent_pattern = r'\d+(\.\d+)?%'
    if any(re.search(percent_pattern, str(v)) for v in column_values if v):
        patterns['is_percentage'] = True
    return patterns
```

2. **Integrate into the Excel parser**:
   - In `src/etl/services/excel_parser.py`, after reading the data, call `detect_patterns` on each column (using the first 100 rows).
   - Store the results in the `data_types` JSON field of `AI_Metadata`.

**Expected output:** The `data_types` field now contains something like `{"Customer_Name": {"is_pan": false, "is_date": false}, "Disbursement_Date": {"is_date": true}}`.

---

## Task 2.1.3 – Source System Identification

**What:** We try to guess which lender/partner the file comes from (e.g., HDFC, SBI) based on file name, sheet names, or column headers.

**Steps:**

1. **Create a source system mapper**:
   - Open `src/ai/services/source_detector.py` and paste:

```python
# src/ai/services/source_detector.py
import re
from typing import List

def detect_source(file_name: str, sheet_names: List[str], headers: List[str]) -> str:
    """Return a likely source system name based on keywords."""
    combined = (file_name + " " + " ".join(sheet_names) + " " + " ".join(headers)).lower()
    if re.search(r'hdfc', combined):
        return "HDFC"
    if re.search(r'sbi|state bank', combined):
        return "SBI"
    if re.search(r'axis', combined):
        return "AXIS"
    if re.search(r'icici', combined):
        return "ICICI"
    if re.search(r'kotak', combined):
        return "KOTAK"
    return "UNKNOWN"
```

2. **Call this function** during file upload and store the result in `AI_Metadata.source_system`.

**Expected output:** After uploading a file named `HDFC_MIS_April.xlsx`, the `source_system` field shows `HDFC`.

---

## Task 2.1.4 – Template Matching

**What:** We compare the current file structure (headers, column order) against previously stored templates to see if it matches a known format.

**Steps:**

1. **Create a template model** (optional – we can just use the `AI_Metadata` table itself). We'll store a "template" as a record where `file_hash` is a placeholder (e.g., `TEMPLATE_<name>`) and `header_columns` is a JSON array.

2. **Implement matching logic**:
   - Open `src/ai/services/template_matcher.py` and paste:

```python
# src/ai/services/template_matcher.py
import json
from sqlalchemy.orm import Session
from src.ai.models import AI_Metadata

def find_matching_template(db: Session, company_id: int, current_headers: list) -> dict:
    """Return the best matching template (metadata record) with confidence."""
    templates = db.query(AI_Metadata).filter(
        AI_Metadata.company_id == company_id,
        AI_Metadata.source_system != "UNKNOWN",
        AI_Metadata.header_columns.isnot(None)
    ).all()
    
    best_match = None
    best_score = 0.0
    for tmpl in templates:
        stored_headers = json.loads(tmpl.header_columns)
        # Compute Jaccard similarity
        intersection = len(set(current_headers) & set(stored_headers))
        union = len(set(current_headers) | set(stored_headers))
        score = intersection / union if union > 0 else 0
        if score > best_score:
            best_score = score
            best_match = tmpl
    return {"template": best_match, "confidence": best_score}
```

3. **Call this after processing a file** and store the result (maybe as a note or in a separate field).

**Expected output:** For a file that matches a known template, you get a high confidence score (e.g., 0.9).

---

## Task 2.1.5 – Confidence Scoring

**What:** We assign a confidence score to each prediction (source system, template match, etc.) so we know how reliable the AI suggestion is.

**Steps:**

1. **Enhance the `AI_Metadata` model** with a `confidence` field (Float).
2. **In each detection step**, compute a confidence value (e.g., based on the number of matching patterns or the strength of the regex).
3. **Store** the confidence in the record.

We already have a confidence from template matching (Jaccard similarity). For source detection, we can assign 0.8 if there is a strong match, 0.5 if fuzzy, etc.

**Expected output:** After processing, each `AI_Metadata` record has a `confidence` score.

---

## Acceptance Criteria (How to know it's done)

- [ ] `AI_Metadata` table exists with columns for file hash, source system, headers, data types, row count, confidence.
- [ ] Uploading a file computes its SHA‑256 hash and stores it (duplicate detection works).
- [ ] Pattern detection identifies dates, PAN, amounts, percentages.
- [ ] Source system is guessed correctly for test files.
- [ ] Template matching returns a known template with a confidence > 0.7 for similar files.

---

## If Stuck (Troubleshooting)

| Problem | Solution |
|---------|----------|
| `alembic` command not found | Run `uv pip install alembic` and try again. |
| Database connection error | Ensure Docker is running and PostgreSQL container is up: `docker-compose ps`. |
| `ModuleNotFoundError: No module named 'src'` | Make sure you are in the root directory (`odos/`) and have `src/` as a package. |
| JSON serialization error | When storing `header_columns` as JSON, use `json.dumps(list)` before saving. |
| File upload fails with 413 (too large) | Check that you have set the file size limit in your API (e.g., FastAPI `max_size`). |
