# Live Workflow Sign-Off (2026-07-20)

## Objective
Validate the complete ETL workflow live, including one-time human approval for a new file type, and ensure UI coverage for operational tables.

## Changes Applied

1. Automated validation during promotion
- File: src/masters/api/etl.py
- Change: Added `_validate_pending_rows(...)` and invoked it from `/api/v1/etl/promote` before promotion.
- Outcome: Stage 5 (validation) is now enforced in the promotion flow even if a separate validation script is not run manually.

2. Added UI screens for rule tables
- File: src/masters/ui/routes_rules.py
- New routes:
  - /masters/rules/validation
  - /masters/rules/commission
  - /masters/rules/commission-slabs
  - /masters/rules/gst
  - /masters/rules/tds

3. Added templates for rule table screens
- src/templates/masters/rules_validation_list.html
- src/templates/masters/rules_commission_list.html
- src/templates/masters/rules_commission_slab_list.html
- src/templates/masters/rules_gst_list.html
- src/templates/masters/rules_tds_list.html

4. Wired router + improved navigation
- File: app/main.py
  - Added `routes_rules` router include.
- File: src/templates/masters/base.html
  - Added nav links for ETL, key masters, and rules UI.

## Live End-to-End Check Performed

### Test Scenario
A brand-new workbook type was generated in memory to force the human-approval branch:
- File name pattern: LIVE_WORKFLOW_CHECK_<timestamp>.xlsx
- Sheet name: Live_<timestamp>
- Data row included valid lender fields (name, PAN, lender code, NBFC)

### Stage Results

1. Upload new file (unknown template)
- Result: HTTP 202 with mapping_required=true
- Status: PASS

2. Analyze (admin)
- Endpoint: /api/admin/mapping/analyze
- Result: HTTP 200 with workbook fingerprint/proposal
- Status: PASS

3. Confirm one-time mapping (human approval)
- Endpoint: /api/admin/mapping/confirm
- Template status used: Active
- Result: HTTP 200, template_id created
- Status: PASS

4. Re-upload same file
- Result: HTTP 200, staged_rows=1, template linked
- Status: PASS

5. Validation
- Trigger: now automatically run within promote endpoint
- Result: validation_summary={pending:1, passed:1, failed:0, warnings:0}
- Status: PASS

6. Promotion + lineage
- Endpoint: /api/v1/etl/promote
- Result: HTTP 200, promoted_count/skipped_count returned
- Lineage endpoint: /api/v1/etl/lineage returned records for batch
- Status: PASS

7. UI visibility
- All verified HTTP 200:
  - /masters/lenders
  - /masters/products
  - /masters/connectors
  - /masters/cases
  - /masters/revenue
  - /masters/commission
  - /masters/payments
  - /masters/rules/validation
  - /masters/rules/commission
  - /masters/rules/commission-slabs
  - /masters/rules/gst
  - /masters/rules/tds
- Status: PASS

8. Data visible check
- API verification (search by lender_name): PASS
- UI verification on /masters/lenders: PASS

## Final Verdict
Workflow is operational end-to-end with human approval flow included.

- New file types: require one-time mapping confirmation (Active template)
- Recurring file types: automated staging -> validation -> promotion
- Canonical data visibility: available in UI screens
- Rule tables UI: now available via /masters/rules/*

## In-Person Finalization Checklist

1. Start app
- python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

2. Open ETL Upload
- http://127.0.0.1:8000/masters/etl/upload

3. For a new format file
- Upload once -> confirm mapping_required
- Run admin mapping analyze/confirm with status=Active
- Re-upload same file

4. Promote batch
- Use Promote action on upload page
- Confirm validation summary in API response and batch status changes

5. Verify data in UI
- /masters/lenders
- /masters/cases
- /masters/revenue
- /masters/commission
- /masters/payments
- /masters/rules/commission
- /masters/rules/commission-slabs

6. Verify evidence
- /api/v1/etl/lineage?batch_guid=<guid>
- /api/v1/etl/errors?batch_guid=<guid>
