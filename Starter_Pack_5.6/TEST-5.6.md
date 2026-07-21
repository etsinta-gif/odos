# TEST-5.6 Tally Integration Test Pack

## Overview
This test pack validates Starter Pack 5.6 for Tally export batch management, export generation, preview, sync and soft delete.

## 1. Setup
- Ensure Sprint 5.5 is completed and the required tables exist:
  - `TRN_TallyExportBatch`
  - `TRN_TallyExportDetail`
- Ensure there is at least one active record in:
  - `TRN_Revenue`
  - `TRN_Commission`
  - `TRN_Expense`
  - `TRN_Payment`
- Run `scripts/seed_test_tally_data.py` to create sample batch records.

## 2. UI Validation
1. Open `http://localhost:8000/masters/tally/exports`
   - Confirm page loads and the Tally Export menu item is visible.
2. Create a new export batch with type `ALL` for a valid period.
3. Open the newly created batch detail page.
4. Click `Generate Export File`.
5. Verify the batch export status becomes `COMPLETED` and exported records are shown.
6. Click `Preview Export` and confirm exported JSON data is displayed.
7. Click `Mark as Synced to Tally` and verify sync status changes to `SYNCED`.
8. Delete the batch and confirm it is removed from the active list.

## 3. API Validation
### Export Batches
1. `POST /api/masters/tally/exports`
   - Payload:
     ```json
     {
       "batch_name": "June 2026 Export",
       "export_type": "ALL",
       "period_start": "2026-06-01",
       "period_end": "2026-06-30",
       "notes": "Test export batch"
     }
     ```
   - Expect `200` and returned batch metadata.
2. `GET /api/masters/tally/exports`
   - Expect the batch created above to appear in the list.
3. `GET /api/masters/tally/exports/{batch_id}`
   - Expect batch details.
4. `POST /api/masters/tally/exports/{batch_id}/generate`
   - Expect export generation success.
5. `GET /api/masters/tally/exports/{batch_id}/details`
   - Expect detail records for each source row.
6. `POST /api/masters/tally/exports/{batch_id}/sync`
   - Expect sync status to update to `SYNCED`.
7. `DELETE /api/masters/tally/exports/{batch_id}`
   - Expect soft delete and batch no longer appears in `GET /api/masters/tally/exports`.

## 4. Edge Cases
- Create a batch with `export_type` of `REVENUE` and verify only revenue records are exported.
- Call `POST /api/masters/tally/exports/{batch_id}/sync` before generation and expect `400`.
- Call `GET /api/masters/tally/exports/{invalid_id}` and expect `404`.

## 5. Expected Results
- Tally export UI and API endpoints function correctly.
- Export batch generation creates detail records.
- Preview page shows output data.
- Sync updates the batch status.
- Batch delete is handled by soft delete only.
