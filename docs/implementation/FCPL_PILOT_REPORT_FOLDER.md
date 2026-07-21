# FCPL Pilot Report (Folder Run)

- Root Folder: C:\Users\etsin\Desktop\1infinity\FinOps - Old Data\Master Data Sheets - For Suresh CFO
- Files Tested: 6
- PASS: 2
- PASS_IGNORE: 3
- PARTIAL: 0
- FAIL*: 1

## Per-File Outcome

| File | Result | Sheet | Mapped | Ignored | Upload | Promote | Error Count |
|---|---:|---|---:|---:|---:|---:|---:|
| 1.RENT FOR FINEOTERIC PVT LTD FY 2026-27.xlsx | PASS_IGNORE | Thane New | 0 | 11 |  |  | 0 |
| Combine Salary Sheet APR-2026.xlsx | PASS_IGNORE | Payroll Sheet | 0 | 67 |  |  | 0 |
| Connector Master - 2026 04 V1.xlsx | FAIL | Master | 2 | 60 | 200 | 400 | 270 |
| DSR - BL AND PL MIS - APRIL_2026.xlsx | PASS | BL | 8 | 22 | 200 | 200 | 0 |
| FCPL - Lender Payout - Master Sheet - 2026 04 V3.4.xlsx | PASS | Master | 17 | 22 | 200 | 200 | 0 |
| Secured Tracker FY 26-27 (2)_1.xlsx | PASS_IGNORE | Tracker | 0 | 79 |  |  | 0 |

## Failure/Partial Details

### Connector Master - 2026 04 V1.xlsx
- Result: FAIL
- Notes: promote did not complete
- Promote Response: {"detail": "No eligible staged records for this batch"}
- Error Samples:
  - [VALIDATION] MST_Connector: PAN must be 10 characters
  - [VALIDATION] MST_Connector: PAN must be 10 characters
  - [VALIDATION] MST_Connector: PAN must be 10 characters
  - [VALIDATION] MST_Connector: PAN must be 10 characters
  - [VALIDATION] MST_Connector: PAN must be 10 characters

