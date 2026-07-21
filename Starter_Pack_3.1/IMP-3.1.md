# IMP-3.1 – Data Extraction

**Document ID:** IMP-3.1  
**Version:** 1.0  
**Status:** Draft  
**Owner:** Aniket (Development Lead)  
**Sprint:** 3.1  
**Phase:** Phase 3 – Canonical ETL Engine  
**Estimated Duration:** 3–4 days

---

## Sprint Overview

**Goal:** Build the first stage of the ETL pipeline: extract data from Excel, CSV, and future API sources into staging tables.

---

## Prerequisites

- [ ] Phase 1 (Sprints 1.1–1.5) completed
- [ ] (Optional) Sprint 2.1 (AI Metadata Learning) completed – not strictly required, but helpful
- [ ] Sample Excel and CSV files ready for testing (e.g., a lender MIS file)

---

## Task 3.1.1 – ETL Framework Skeleton

**What:** Create the core ETL engine that orchestrates extraction, validation, and loading. For now, we focus on extraction.

### Steps

1. **Open VS Code** and open the `odos` folder.

2. **Open the terminal** (View → Terminal or press `` Ctrl+` ``).

3. **Activate virtual environment** (if using `uv`):
   ```
   > source .venv/bin/activate
   ```
   (On Windows: `.venv\Scripts\activate`)

4. **Create the ETL engine module**:
   - Open `src/etl/engine.py` (if the folder/file doesn't exist, create it).
   - Paste the following code:

```python
# src/etl/engine.py
from typing import Dict, Any, List
from src.etl.services.excel_extractor import extract_excel
from src.etl.services.csv_extractor import extract_csv
from src.etl.services.api_extractor import extract_api
from src.etl.models import ETL_ImportBatch, ETL_StagingRawData
from src.core.database import SessionLocal

class ETLPipeline:
    def __init__(self, batch_id: str, company_id: int):
        self.batch_id = batch_id
        self.company_id = company_id
        self.db = SessionLocal()

    def extract(self, source_type: str, source_path: str, **kwargs) -> List[Dict[str, Any]]:
        """Extract data from source and return list of rows."""
        if source_type == "excel":
            return extract_excel(source_path, **kwargs)
        elif source_type == "csv":
            return extract_csv(source_path, **kwargs)
        elif source_type == "api":
            return extract_api(source_path, **kwargs)
        else:
            raise ValueError(f"Unsupported source type: {source_type}")

    def load_staging(self, rows: List[Dict[str, Any]], target_table: str):
        """Store extracted rows into staging table."""
        # We will implement this in later sprints (3.4)
        pass

    def close(self):
        self.db.close()
```

5. **Verify the ETL models exist**:  
   - Open `src/etl/models.py`. If it doesn't exist, create it with the `ETL_ImportBatch` and `ETL_StagingRawData` models (they were stubbed in Sprint 1.5). For now, you can just leave it empty if you already have them from Phase 1.

6. **Create an API endpoint to trigger extraction** (optional for testing):
   - In `src/etl/api/etl.py`, add a new endpoint (you can create the file if it doesn't exist):

```python
# src/etl/api/etl.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.etl.engine import ETLPipeline

router = APIRouter(prefix="/etl", tags=["ETL"])

@router.post("/extract")
def start_extraction(file_id: str, source_type: str, db: Session = Depends(get_db)):
    # For now, just create a batch and run extraction
    # We'll implement batch creation later
    return {"message": "Extraction started (stub)"}
```

**Expected output:** When you call `POST /etl/extract` with parameters, you get a JSON response `{"message": "Extraction started (stub)"}`.

**Troubleshooting:**
- If you get `ModuleNotFoundError: No module named 'src'`, ensure you are in the root directory and have `src/` as a package.
- If the database session fails, check that Docker containers are running (`docker-compose ps`).

---

## Task 3.1.2 – Excel Extraction

**What:** Parse an Excel file, read all rows, and return a list of dictionaries.

### Steps

1. **Create `src/etl/services/excel_extractor.py`**:

```python
# src/etl/services/excel_extractor.py
import pandas as pd
from typing import List, Dict, Any

def extract_excel(file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
    """Extract data from Excel file and return list of rows as dicts."""
    if sheet_name is None:
        # Use the first sheet
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    # Convert to list of dicts
    records = df.to_dict(orient='records')
    return records
```

2. **Install required library** if not present:
   ```
   > uv pip install pandas openpyxl
   ```

3. **Test the function** in a Python shell:
   - Open a Python interpreter:
     ```
     > python
     ```
   - Run:
     ```python
     from src.etl.services.excel_extractor import extract_excel
     rows = extract_excel('path/to/your/sample.xlsx')
     print(len(rows))
     print(rows[0])
     ```
   - Expected output: prints the number of rows and the first row as a dict.

**Troubleshooting:**
- If `ModuleNotFoundError: No module named 'openpyxl'`, install it: `uv pip install openpyxl`.
- If you get a `FileNotFoundError`, check the file path.

---

## Task 3.1.3 – CSV Extraction

**What:** Parse a CSV file and return rows.

### Steps

1. **Create `src/etl/services/csv_extractor.py`**:

```python
# src/etl/services/csv_extractor.py
import csv
from typing import List, Dict, Any

def extract_csv(file_path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
    """Extract data from CSV file."""
    rows = []
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            rows.append(row)
    return rows
```

2. **Test** with a sample CSV file (you can create one with columns like `Name,Age,City`).

---

## Task 3.1.4 – API Extraction (stub)

**What:** Prepare a placeholder for future API integration.

### Steps

1. **Create `src/etl/services/api_extractor.py`**:

```python
# src/etl/services/api_extractor.py
import requests
from typing import List, Dict, Any

def extract_api(url: str, headers: dict = None, params: dict = None) -> List[Dict[str, Any]]:
    """Extract data from REST API (placeholder)."""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    # Assume data is a list of objects
    return data
```

2. **Install requests** if not already installed:
   ```
   > uv pip install requests
   ```

3. **Note:** This is only a stub; actual implementation will depend on specific APIs (to be added later).

---

## Task 3.1.5 – File Validation

**What:** Before extraction, validate that the file format is correct and the required columns exist.

### Steps

1. **Create `src/etl/validators/file_validator.py`**:

```python
# src/etl/validators/file_validator.py
import os

def validate_file(file_path: str, allowed_extensions: list = ['.xlsx', '.xls', '.csv']):
    """Check file extension and existence."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {ext}. Allowed: {allowed_extensions}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return True
```

2. **Integrate into the ETL pipeline** by calling this function before extraction.

---

## Task 3.1.6 – Batch Processing

**What:** Process extraction in chunks to avoid memory issues with large files.

### Steps

1. **Modify the Excel extractor to support chunking** – update `excel_extractor.py`:
```python

def extract_excel_chunked(file_path: str, sheet_name: str = None, chunk_size: int = 1000):
    """Yield rows in chunks."""
    if sheet_name is None:
        for chunk in pd.read_excel(file_path, engine='openpyxl', chunksize=chunk_size):
            yield chunk.to_dict(orient='records')
    else:
        for chunk in pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', chunksize=chunk_size):
            yield chunk.to_dict(orient='records')
```

2. **Update the ETL pipeline** to use chunked extraction for large files (optional for now; we can add a flag).

---

## Acceptance Criteria

- [ ] `ETLPipeline` class exists with `extract` method that supports Excel, CSV, and API.
- [ ] Excel extraction returns a list of dicts for a given file.
- [ ] CSV extraction works similarly.
- [ ] File validation rejects unsupported file types.
- [ ] (Optional) Chunked extraction works for large Excel files.

---

## If Stuck (Troubleshooting)

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'pandas'` | Run `uv pip install pandas` |
| `ModuleNotFoundError: No module named 'openpyxl'` | Run `uv pip install openpyxl` |
| CSV encoding error | Specify `encoding='utf-8'` or `'latin-1'` in `open()`. |
| MemoryError with large Excel | Use the chunked approach; avoid loading all rows at once. |
| API extraction fails | Ensure `requests` is installed: `uv pip install requests`. |
| PermissionError when reading file | Check that the file path exists and has read permissions. |
| `sqlalchemy.exc.OperationalError` | Ensure PostgreSQL is running: `docker-compose up -d`. |
