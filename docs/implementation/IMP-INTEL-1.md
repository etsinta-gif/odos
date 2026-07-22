# IMP-INTEL-1 - ODOS Intelligence Layer (Simplified Core)

Document ID: IMP-INTEL-1  
Version: 1.0  
Status: Draft  
Owner: Implementation Pack Engineer  
Sprint: INTEL-1  
Phase: Phase 7 - Intelligence Layer  
Estimated Duration: 10-12 days (fresher)

## Sprint Overview

Goal: transform ODOS into a flexible cross-verification intelligence layer that ingests CRM, accounting, MIS, lender, and bank data; verifies against defaults; generates red flags; and supports flexible BI.

### Scope Direction
- Keep: ETL pipeline, mapping engine, multi-target promotion, RBAC, UI-1 foundations, multi-tenancy, existing tests.
- Adapt: party defaults and transaction tables for reported vs verified values plus flexible JSON fields.
- De-scope from active ownership: RUL commission/slab/GST/TDS calculation behavior, rate cards, slab calculation paths.
- Add: cross-verification service, red-flag lifecycle APIs, UI actions, documentation and tests.

## Deliverables

| File | Path | Purpose |
|---|---|---|
| Updated Party Models | src/masters/models.py | Add defaults (GST, TDS, max commission) and metadata |
| Updated Transaction Models | src/transactions/models.py | Revenue/Commission/Payment reported vs system fields + flexible JSON |
| Red Flag Model | src/etl/models.py | ETL_RedFlag table |
| Cross-Verification Service | src/etl/services/cross_verify.py | GST/TDS/commission checks |
| Promoter Integration | src/etl/services/promoter.py | Invoke cross-verification during promotion |
| Alerts API | src/alerts/api/alerts.py | List, summary, resolve, ignore red flags |
| ETL API Integration | src/masters/api/etl.py | Integrate promoted verification/red-flag outcomes |
| Red Flag UI | frontend/src/pages/RedFlags/ | Dashboard, filters, resolve/ignore |
| Party UI | frontend/src/pages/Party/ | View/edit defaults |
| Migrations | alembic/versions/ | Schema updates |
| Tests | tests/test_cross_verify.py | Verification and red-flag unit tests |
| Documentation | docs/INTELLIGENCE_LAYER.md | Operating model and workflows |

## Implementation Plan

### Phase 1: Data Model Updates (Day 1-2)

1. Add a unified party/defaults model strategy.
- Preferred approach for this codebase: extend existing party-like master entities without breaking current MST_* structure.
- If introducing MST_Party, ensure migration and API mapping do not break existing lenders/connectors/customers.

2. Add verification-ready transaction fields.
- Revenue: reported_amount, reported_gst, reported_tds, reported_net, system_gst, system_tds, gst_match, tds_match, data.
- Commission: reported_commission, reported_gst, reported_tds, reported_net, exceeds_max, gst_match, tds_match, data.
- Payment: core payment fields and flexible data.

3. Add ETL_RedFlag model.
- Include company scope, source linkage (batch/record), severity/category/message, reported vs expected values, and resolution metadata.

### Phase 2: Cross-Verification Service (Day 2-4)

Create src/etl/services/cross_verify.py with:
- verify_revenue(revenue_data, party_defaults)
- verify_commission(commission_data, party_defaults)
- create_red_flags(...)
- clear severity and category conventions: CRITICAL/WARNING/INFO and gst/tds/commission/missing/duplicate.
- small tolerance for decimal rounding mismatch.

### Phase 3: Promotion Integration (Day 4-5)

Update promoter paths so that for revenue/commission:
- party/default context is resolved.
- cross-verification runs before final commit.
- verification outcomes are persisted in TRN_* rows.
- red flags are inserted to ETL_RedFlag in same unit-of-work.

### Phase 4: Alerts API (Day 5-6)

Add src/alerts/api/alerts.py with endpoints:
- GET /api/alerts/red-flags
- GET /api/alerts/red-flags/summary
- PUT /api/alerts/red-flags/{flag_id}/resolve
- PUT /api/alerts/red-flags/{flag_id}/ignore

Requirements:
- enforce auth and tenant/company scoping.
- support filters for severity/category/status.
- persist resolved_by/resolved_at/resolution_notes.

### Phase 5: UI Updates (Day 6-9)

1. Red Flag Dashboard.
- summary cards, filter by severity/status, list with context and timestamps.
- resolve/ignore actions with notes.

2. Party Defaults UI.
- list and edit party defaults for GST/TDS/max commission.
- must use existing auth + tenant context.

### Phase 6: Migrations and Tests (Day 9-10)

1. Create and apply migration.
- alembic revision --autogenerate -m "intelligence_layer_schema_changes"
- alembic upgrade head

2. Add tests.
- tests/test_cross_verify.py covering gst mismatch, tds mismatch, commission exceeds max, and matching scenarios.
- include tenancy and persistence checks for red flags.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | Party defaults fields available and editable |
| 2 | Transaction tables include reported and verified fields |
| 3 | ETL promotion performs cross-verification |
| 4 | Red flags are generated for mismatches |
| 5 | Red flag dashboard shows summary and details |
| 6 | Resolve/ignore workflows function with audit metadata |
| 7 | Party defaults updates affect subsequent verifications |
| 8 | Flexible JSON fields are persisted and queryable |
| 9 | Existing regression suite passes |
| 10 | docs/INTELLIGENCE_LAYER.md published |

## Runbook Commands

```bash
# Migrations
alembic upgrade head

# Focused tests
pytest tests/test_cross_verify.py -v

# Full tests
pytest -v

# Backend (this repo)
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## Notes for This Repository

- Current codebase has strong existing MST_* structures and historical RUL_* usage. De-scope should be feature-gated first, then cleanup after telemetry confidence.
- Current API contracts and tests must remain backward compatible where possible.
- Keep tenant isolation mandatory on all new endpoints and queries.

## Handoff

1. Execute phases in order.
2. Run full tests and smoke flows.
3. Validate with sample mismatch files and expected red flags.
4. Share results using TEST-INTEL-1 report template.
