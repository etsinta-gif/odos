=============================================
SPRINT 5.6 STARTER PACK
=============================================

This is the starter pack for Sprint 5.6 – Tally Integration.

PREREQUISITES:
- Sprint 5.5 completed (Expense & Payment Management UI)
- TRN_TallyExportBatch and TRN_TallyExportDetail tables exist
- TRN_Revenue, TRN_Commission, TRN_Expense, TRN_Payment tables populated
- MST_TallyMapping table exists

WHAT YOU WILL BUILD:
- Tally export batch management (create export batches, view status)
- Export financial data to Tally-compatible XML/JSON format
- Track export status (PENDING, EXPORTED, SYNCED, FAILED)
- Preview export data before finalizing

STEPS:
1. Copy ALL files and folders from this pack into your odos project root
2. Follow IMP-5.6.md step by step
3. Start the server and test at http://localhost:8000/masters/tally/exports

FILES INCLUDED:
- src/masters/api/tally.py       (Tally export batch & detail APIs)
- src/masters/ui/routes.py        (UI routes – you will ADD new routes)
- src/templates/masters/*.html    (Tally batch list, detail, preview)
- scripts/seed_test_tally_data.py (Optional test data)

ESTIMATED DURATION: 2 days
CONTACT: CTO or Technical Programme Manager
