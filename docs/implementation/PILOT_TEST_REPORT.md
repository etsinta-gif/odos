# PILOT_TEST_REPORT

Document ID: PILOT-TEST-5.9
Date: 2026-07-20
Environment: Local ODOS (SQLite, FastAPI TestClient)
Scope: One-by-one pilot with real workspace Excel files (excel-agnostic behavior validation)

## 1. Files Tested (One-by-One)
1. samples/Lender_Master.xlsx
2. samples/Connector_Master.xlsx
3. samples/Secured_Tracker.xlsx
4. samples/Empty_File.xlsx

## 2. Overall Verdict
- Pilot readiness: PARTIAL PASS
- Core ingestion path works for lender and secured tracker files.
- Excel-agnostic ignore behavior works correctly for irrelevant/empty file.
- Connector file promotion was blocked by active validation rule mismatch (PAN required), which is a rule configuration issue, not a pipeline crash.

## 3. Health and Core Checks
- GET /api/v1/health: PASS (200, status ok)
- Mapping analyze endpoint: PASS on all 4 files
- Template confirm/approve/activate: PASS on files with relevant mappings
- ETL upload: PASS on 3 relevant files
- Validation + Promotion:
  - Lender: PASS
  - Secured Tracker: PASS
  - Connector: PARTIAL (validation fail, promotion blocked)
- Lineage endpoint: PASS

## 4. Per-File Results

## 4.1 Lender Master
- File: samples/Lender_Master.xlsx
- Sheet used: Master
- Mapping proposal: 6 mapped, 0 ignored
- Template: created and activated (template_id=13)
- Upload #1: PASS
  - batch_guid: 74cd004c-266d-46b3-a919-d168b9aa78a7
  - staged_rows: 6
- Promote #1: PASS
  - promoted_count: 6
  - skipped_count: 0
- Lineage #1: 2 rows
- Re-upload #2: PASS
  - batch_guid: a59292f8-ba98-43d3-b014-c8b107551808
- Promote #2: PASS
  - promoted_count: 6
  - skipped_count: 0
- Lineage #2: 2 rows
- Status: PASS

## 4.2 Connector Master
- File: samples/Connector_Master.xlsx
- Sheet used: Master
- Mapping proposal: 5 mapped, 1 ignored
- Template: created and activated (template_id=14)
- Upload #1: PASS
  - batch_guid: c5341096-0d26-454b-85f6-ecba2f6bf40e
  - staged_rows: 5
- Validation outcome: FAILED for all staged rows due active rule
  - ETL_ErrorLog evidence: 5 errors
  - Error: PAN must be 10 characters
- Promote #1: blocked (no eligible staged records)
- Re-upload #2: PASS staging, same validation failure
  - batch_guid: c643232e-6d12-44eb-a131-2065b73a782d
- Promote #2: blocked (no eligible staged records)
- Lineage: 0 (expected when promotion blocked)
- Status: PARTIAL

## 4.3 Secured Tracker
- File: samples/Secured_Tracker.xlsx
- Sheet used: Master
- Mapping proposal: 5 mapped, 2 ignored
- Template: created and activated (template_id=15)
- Upload #1: PASS
  - batch_guid: 4aab89bd-3676-420e-9439-d39b8796f17a
  - staged_rows: 2
- Promote #1: PASS
  - promoted_count: 2
  - skipped_count: 0
- Lineage #1: 2 rows
- Re-upload #2: PASS
  - batch_guid: 03a054b0-1dc6-4599-b4ad-e9f4080fab96
- Promote #2: PASS
  - promoted_count: 2
  - skipped_count: 0
- Lineage #2: 2 rows
- Status: PASS

## 4.4 Empty/Irrelevant File
- File: samples/Empty_File.xlsx
- Sheet used: Sheet1
- Mapping proposal: 0 mapped, 2 ignored
- Behavior: correctly classified as not relevant and ignored
- Status: PASS_IGNORE

## 5. Excel-Agnostic Behavior Validation
Expected behavior from CFO/CTO direction: if input is not relevant, system should return no mapping relevance and ignore.

Observed:
- Empty_File.xlsx returned 0 mapped columns and was ignored.
- System did not crash, and no invalid ETL promotion occurred.
- This confirms excel-agnostic + safe-ignore behavior.

## 6. Issues Found
1. Connector template mapped file does not include PAN values, but an active validation rule enforces PAN length = 10 on MST_Connector rows.
2. Result: all connector rows failed validation and promotion did not proceed.

Impact:
- Pipeline is stable, but connector onboarding is blocked until rule/mapping alignment is done.

## 7. Recommendations Before Next Pilot Iteration
1. Adjust rule scope for MST_Connector PAN rule to be conditional or warning where source files intentionally do not provide PAN.
2. Add table-profile based rule packs (per template type) so connector onboarding uses a connector-specific mandatory set.
3. For idempotency verification, re-test connector after rule alignment; current lender/tracker runs already show stable repeat processing.

## 8. Evidence Artifacts Saved
- Structured pilot result JSON:
  - docs/pilot_run_results_final.json
- Intermediate pilot output:
  - docs/pilot_run_results.json
  - docs/pilot_run_results_v2.json

## 9. Final Pilot Conclusion
- Lender Master: PASS
- Secured Tracker: PASS
- Connector Master: PARTIAL (validation-rule mismatch)
- Irrelevant/empty input handling: PASS

Go/No-Go Recommendation:
- GO for next phase with condition: finalize connector validation-rule policy first, then rerun connector pilot once.
