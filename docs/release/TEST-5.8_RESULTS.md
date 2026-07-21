# TEST-5.8 Execution Report (Rerun After 5.8.2 Patch)

Date: 2026-07-20
Tester: Copilot-assisted run
Scope: Generic Excel Mapping Engine

## Environment
- Workspace app entrypoint used: `app/main.py`
- Python: 3.14.6 (.venv)
- API test mode: FastAPI `TestClient`
- Sample files created under `samples/`

## Unit Test Evidence
- Command executed:
  - `python -m pytest tests/test_mapping_engine.py -v`
- Result:
  - `10 passed`

## Test Case Results

| Test ID | Status | Actual Result |
|---|---|---|
| TC-UNIT-001 | Pass | Unit tests expanded and passed (`10 passed`). |
| TC-CLI-001 | Pass | `scripts/analyze_excel.py -g` succeeded; slab mapping detected. |
| TC-CLI-002 | Pass | Without `-g`, output is metadata-only (proposal fields remain null). |
| TC-CLI-003 | Pass | Non-existent sheet returns non-zero and error. |
| TC-API-053 | Pass | Analyze endpoint returned HTTP 200 with sheet analysis payload. |
| TC-API-054 | Pass | Accuracy checks passed for key business headers: `Lender / NBFC`, `NBFC?`, and PAN pattern mapping (`suggestions=6` on 6-column sample). |
| TC-API-055 | Pass | Slab columns detected and mapped to `RUL_CommissionSlab.rate` with expected confidence. |
| TC-API-056 | Pass | Template confirm endpoint created template successfully. |
| TC-API-057 | Pass | Template list endpoint returned created template. |
| TC-API-058 | Pass | Get template by id successful. |
| TC-API-059 | Pass | Update template by id successful. |
| TC-API-060 | Pass | Delete template successful and template removed from list output. |
| TC-ETL-001 | Pass | ETL upload with stored mapping returned HTTP 200. |
| TC-ETL-002 | Pass | Staging rows contain mapped lender fields and slab rows (`MST_Lender`, `RUL_CommissionSlab`). |
| TC-ETL-003 | Pass | Promotion succeeded and persisted slab data to `RUL_CommissionSlab` (`slab_count=2`). |
| TC-EDGE-023 | Pass | Empty file analysis returns HTTP 200 without crash. |
| TC-EDGE-024 | Pass | Unsupported format returns HTTP 400. |
| TC-EDGE-025 | Pass | Missing sheet returns HTTP 400. |
| TC-EDGE-026 | Pass | Large file test used 14.55 MB workbook; analyze returned HTTP 200 in 0.14s. |

## Summary
- Total test cases: 19
- Passed: 19
- Failed: 0
- Blocked: 0
- Pass rate: 100%

## Critical Failures
- None

## Key Observations
1. First-time mapping workflow and template CRUD are functional.
2. Repeat-run ingestion now stages both base entities and slab rows when slab mappings are present.
3. Promotion now persists slab mappings into `RUL_CommissionSlab` and remains duplicate-safe for repeat batches.
4. Template lookup now prefers latest active template by fingerprint/pattern, improving approval-to-runtime consistency.
5. Analyzer now samples rows per sheet for metadata inference, significantly improving large-file response time.

## Artifacts
- `samples/Lender_Master.xlsx`
- `samples/Connector_Master.xlsx`
- `samples/Secured_Tracker.xlsx`
- `samples/Empty_File.xlsx`
- `samples/Mixed_Types.xlsx`
- `samples/Large_File_10MB.xlsx`
- `docs/release/TEST-5.8_RESULTS.md`
