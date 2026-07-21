# TRACKER_MAPPING_APPROVAL_REPORT

Date: 2026-07-20
Scope: Human approval report for sheet-level mapping (Secured Tracker example)
Source file: samples/Secured_Tracker.xlsx
Selected sheet: Master
Entity type used in pilot: TRN_Case
Template used: template_id=15 (Active)

## 1. Column Summary (Tracker Sheet: Master)
- Total columns found in sheet: 7
- Mapped to schema: 5
- Ignored: 2

## 2. Mapped Fields (For Human Approval)
| # | Excel Source Column | Target Table | Target Field | Confidence | Rule/Reason |
|---|---|---|---|---:|---|
| 1 | case_number | TRN_Case | case_number | 95 | Exact normalized match |
| 2 | customer_name | MST_Connector | full_name | 92 | Alias match with 'full_name' |
| 3 | sanction_amount | TRN_Case | sanction_amount | 95 | Exact normalized match |
| 4 | disbursement_amount | TRN_Case | disbursement_amount | 95 | Exact normalized match |
| 5 | status | TRN_Case | status | 95 | Exact normalized match |

Approval intent:
- Approver validates semantic correctness of each source-to-target mapping.
- If accepted, template status remains Active and repeat uploads auto-apply this mapping.

## 3. Ignored Fields
| # | Excel Source Column | Ignore Status | Reason |
|---|---|---|---|
| 1 | disbursement_date | Ignored | No mapping found |
| 2 | application_date | Ignored | No mapping found |

Action choice for approver:
- Keep ignored as-is if fields are not required for current target schema.
- Add explicit mapping/transformation rules if these fields become mandatory.

## 4. Multi-Sheet Excel Handling (What Was Done)
- In pilot execution, explicit sheet was used per file (Tracker used `Master`).
- Analyzer can process:
  - One sheet when `sheet_name` is provided.
  - All sheets when `sheet_name` is not provided.
- Upload behavior:
  - Workbook fingerprint is computed using all sheets.
  - Actual row ingestion uses only the template sheet (`template.sheet_name`).

Practical effect:
- Intro/Info sheets do not get ingested if template points to `Master`.
- If wrong/default sheet is used at analyze time, mapping relevance may degrade.

## 5. Pilot Evidence Snapshot
- Tracker result: PASS
- Analyzer output for Tracker: mapped=5, ignored=2
- Promotion succeeded in both runs for Tracker batches.

Cross-file pilot count reference:
- Lender_Master.xlsx: mapped=6, ignored=0
- Connector_Master.xlsx: mapped=5, ignored=1
- Secured_Tracker.xlsx: mapped=5, ignored=2
- Empty_File.xlsx: mapped=0, ignored=2 (safe ignore)

## 6. Approval Decision Block
- Decision: APPROVE / REJECT / APPROVE WITH CHANGES
- Reviewer name:
- Review date:
- Notes:

Recommended default for current Tracker mapping: APPROVE
(Reason: Mapping quality high, confidence >= 92 for all mapped fields, pilot promote PASS.)
