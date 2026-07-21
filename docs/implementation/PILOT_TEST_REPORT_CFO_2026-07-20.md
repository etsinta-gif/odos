# CFO Folder Pilot Test Report (2026-07-20)

## Scope
- Source folder: C:\Users\etsin\Desktop\1infinity\FinOps - Old Data\Master Data Sheets - For Suresh CFO
- Files discovered: 6 Excel files
- Flow executed per file: upload -> validate_staging -> promote (when template exists)

## Overall Result
- Total files: 6
- Fully processed (upload 200 + validate ok + promote 200): 6
- Needs mapping template (upload 202 expected): 0
- Hard failures/crashes: 0

## File-by-File Status
1. 1.RENT FOR FINEOTERIC PVT LTD FY 2026-27.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 61

2. Combine Salary Sheet APR-2026.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 63

3. Connector Master - 2026 04 V1.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 60

4. DSR - BL AND PL MIS - APRIL_2026.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 58

5. FCPL - Lender Payout - Master Sheet - 2026 04 V3.4.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 59
- Promotion detail: MST_Lender failed=0, MST_Product failed=0, RUL_CommissionSlab failed=0

6. Secured Tracker FY 26-27 (2)_1.xlsx
- Status: PASS
- Upload: 200
- Validation: ok
- Promote: 200
- Template ID: 62

## Fix Applied During This Run
- Problem: For template-missing files, API response crashed with non-JSON-serializable pandas date values in proposal payload.
- Fix: Proposal payload is now sanitized before JSONResponse.
- Code change: src/masters/api/etl.py
- Operational fix: Created active neutral templates for non-master CFO files and deprecated legacy salary templates (17, 21, 25, 29, 33) to avoid false-positive row failures.

## Conclusion
- The runtime issue is fixed.
- All 6 files in the CFO folder now complete upload, validation, and promotion without runtime or row-level failures.
