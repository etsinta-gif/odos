# TEST-UI-1 Live Smoke Report

Date: 2026-07-21
Scope: Hybrid ETL live path verification with governance workflow

## Environment
- Backend: http://127.0.0.1:8000
- Frontend: http://127.0.0.1:3000
- Python Env: venv (project)

## Test Case: Dynamic Mapping -> Draft -> Submit -> Activate -> Strict Reupload

### Inputs
- User: newly registered tenant admin
- File: samples/_synthetic_phase5/UI1_LIVE3_UNKNOWN_LENDER.xlsx
- Upload mode: auto_process=true

### Results
1. Register: PASS (200)
2. Login: PASS (200)
3. First Upload (unknown template): PASS
   - HTTP 200
   - status = mapping_required
   - mode = dynamic_mapping
4. Save Draft: PASS (200)
5. Submit for Approval: PASS (200)
   - status = Approved
6. Activate Template: PASS (200)
   - status = Active
7. Re-upload same file: PASS
   - HTTP 200
   - status = success
   - mode = strict_template

## Additional Endpoint Checks
- GET /api/v1/health: PASS (200)
- GET /api/masters/dashboard/stats: PASS (200)
- GET /api/admin/redflags: PASS (200)

## Defects Found During Earlier Run and Fixed
1. Template pattern matching false negatives due double-escaped regex patterns.
   - Fixed in src/metadata/services/field_mapper.py
2. Unknown CSV upload crashed with 500 in hybrid analysis path.
   - Fixed in src/masters/api/etl.py with CSV analysis fallback.

## Final Status
- Hybrid ETL behavior is operational in live environment.
- Path B governance flow is operational.
- Transition from Path B to Path A validated by re-upload behavior.
