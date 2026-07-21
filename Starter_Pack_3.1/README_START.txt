=============================================
SPRINT 3.1 STARTER PACK
=============================================

This is the starter pack for Sprint 3.1 – Data Extraction.

PREREQUISITES:
- Phase 1 (Sprints 1.1–1.5) completed
- (Optional) Sprint 2.1 completed for better metadata
- Docker containers running (postgresql, redis)
- Python 3.12+ and uv installed

STEPS:
1. Unzip this folder into your project root (odos/)
2. Copy the stub files into the correct locations
3. Install required libraries: uv pip install pandas openpyxl requests
4. Follow IMP-3.1.md step by step

FILES INCLUDED:
- src/etl/engine.py                      (ETL pipeline skeleton)
- src/etl/services/excel_extractor.py    (Excel extraction)
- src/etl/services/csv_extractor.py      (CSV extraction)
- src/etl/services/api_extractor.py      (API extraction stub)
- src/etl/validators/file_validator.py   (File validation)

ESTIMATED DURATION: 3–4 days
CONTACT: CTO or Technical Programme Manager
