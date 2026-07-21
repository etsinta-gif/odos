=============================================
SPRINT 5.10 STARTER PACK
=============================================

This pack adds multi-target ETL promotion for supported runtime tables:
- MST_Lender
- MST_Product
- RUL_CommissionRule
- RUL_CommissionSlab

PREREQUISITES:
- IMP-5.9 applied
- Template 16 present and active for the FCPL lender payout file
- Reference seed CSV loaded if you intend to use reference lookup extensions

STEPS:
1. Run migrations: alembic upgrade head
2. Load data/reference_seed.csv if needed
3. Start the app
4. Upload the FCPL lender payout workbook
5. Validate staging
6. Promote the batch via /api/v1/etl/promote or scripts/promote_staging.py

NOTES:
- The current runtime implements multi-target promotion for the supported tables above.
- REF_* resolution scaffolding is included, but the core 5.10 path does not yet persist reference foreign keys because the current runtime master/rule tables do not expose those FK columns.