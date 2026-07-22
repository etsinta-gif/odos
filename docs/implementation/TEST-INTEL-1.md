# TEST-INTEL-1 - ODOS Intelligence Layer (Simplified Core)

Document ID: TEST-INTEL-1  
Version: 1.0  
Status: Ready for Execution  
Owner: Aniket (Testing)  
Sprint: INTEL-1  
Phase: Phase 7 - Intelligence Layer  
Estimated Duration: 2-3 days

## 1. Test Plan

### 1.1 Scope
In scope:
- Party defaults updates (GST, TDS, max commission).
- Revenue and commission cross-verification outcomes.
- Red-flag generation and lifecycle APIs.
- Red-flag dashboard filtering/actions.
- Party defaults UI view/edit flow.
- ETL promotion integration for cross-verification.
- Flexible JSON field persistence.

Out of scope:
- Performance benchmarking.
- Advanced BI semantic-layer completeness.
- Historical legacy report parity.

### 1.2 Environment
- Backend: FastAPI local server.
- Frontend: React app local server.
- DB: current project SQLAlchemy backend with migrations applied.
- Browser: latest Chrome.
- Tools: Swagger, curl, terminal.

### 1.3 Test Data Baseline
- Admin user and ops user.
- One lender/party default profile:
  - default_gst_rate = 18.0
  - default_tds_rate = 10.0
  - max_commission = 5000
- Revenue sample:
  - reported_amount = 10000
  - reported_gst = 1800 (match)
  - reported_tds = 1000 (match)
- Commission sample:
  - reported_commission = 6000 (exceeds max)
- Revenue mismatch sample:
  - reported_gst = 100 (mismatch)

### 1.4 Priority Order
1. Schema and model validation (P0)
2. Cross-verification service checks (P0)
3. Red-flag persistence (P0)
4. Alerts APIs (P0)
5. ETL promotion integration (P0)
6. UI checks (P1)

### 1.5 Entry Criteria
- INTEL-1 code merged in test branch.
- Migrations applied.
- Backend and frontend running.

### 1.6 Exit Criteria
- All P0 test cases pass.
- P1 pass rate >= 80%.
- No unresolved critical defects.

## 2. Test Cases

### 2.1 Schema and Models (P0)
- TC-SCH-001: Party defaults fields exist.
- TC-SCH-002: Revenue verification columns exist.
- TC-SCH-003: ETL_RedFlag table exists.

### 2.2 Cross-Verification Service (P0)
- TC-CV-001: GST correct -> gst_match true, no GST red flag.
- TC-CV-002: GST mismatch -> gst_match false, WARNING gst red flag.
- TC-CV-003: TDS mismatch -> tds_match false, WARNING tds red flag.
- TC-CV-004: Commission exceeds max -> exceeds_max true, CRITICAL commission red flag.

### 2.3 Alerts API (P0)
- TC-API-061: GET red flags unauthenticated -> 401.
- TC-API-062: GET red flags authenticated + filters -> 200 and filtered results.
- TC-API-063: GET summary -> includes total/critical/warning/info/open/resolved/ignored.
- TC-API-064: Resolve flag -> status RESOLVED with resolver metadata.
- TC-API-065: Ignore flag -> status IGNORED with resolver metadata.

### 2.4 ETL Integration (P0)
- TC-ETL-010: Revenue promotion runs verification and persists system fields.
- TC-ETL-011: Commission promotion exceeds max and generates CRITICAL flag.

### 2.5 UI (P1)
- TC-UI-077: Red flag dashboard loads summary and list.
- TC-UI-078: Severity/status filters update list.
- TC-UI-079: Resolve action updates status.
- TC-UI-080: Party defaults columns visible.
- TC-UI-081: Edit defaults persists and influences new verifications.

### 2.6 Regression (P0)
- TC-REG-003: Legacy ETL flows still pass for non-verification datasets.
- TC-REG-004: Flexible JSON data preserved and retrievable.

## 3. Execution Commands

```bash
# Apply schema
alembic upgrade head

# Focused tests
pytest tests/test_cross_verify.py -v

# Full regression
pytest -v

# Backend
uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

## 4. Report Template

Date: __________  
Tester: Aniket

| Test ID | Description | Priority | Pass/Fail | Notes |
|---|---|---|---|---|
| TC-SCH-001 | Party defaults fields | P0 |  |  |
| TC-SCH-002 | Revenue verification fields | P0 |  |  |
| TC-SCH-003 | Red flag table | P0 |  |  |
| TC-CV-001 | GST match path | P0 |  |  |
| TC-CV-002 | GST mismatch path | P0 |  |  |
| TC-CV-003 | TDS mismatch path | P0 |  |  |
| TC-CV-004 | Commission max breach | P0 |  |  |
| TC-API-061 | Unauth red flags | P0 |  |  |
| TC-API-062 | Auth filtered red flags | P0 |  |  |
| TC-API-063 | Red flag summary | P0 |  |  |
| TC-API-064 | Resolve red flag | P0 |  |  |
| TC-API-065 | Ignore red flag | P0 |  |  |
| TC-ETL-010 | Revenue cross-verify in promote | P0 |  |  |
| TC-ETL-011 | Commission max check in promote | P0 |  |  |
| TC-UI-077 | Red flag dashboard load | P1 |  |  |
| TC-UI-078 | Red flag filtering | P1 |  |  |
| TC-UI-079 | Resolve via UI | P1 |  |  |
| TC-UI-080 | Party defaults display | P1 |  |  |
| TC-UI-081 | Party defaults edit | P1 |  |  |
| TC-REG-003 | Legacy ETL compatibility | P0 |  |  |
| TC-REG-004 | Flexible JSON persistence | P0 |  |  |

Overall Status: PASS / FAIL

## 5. Troubleshooting Quick Guide

| Symptom | Likely Cause | Action |
|---|---|---|
| No cross-verification results | cross_verify not called by promoter | check integration path in promoter and commit flow |
| Flags not visible | company scope mismatch | verify user company and inserted company_id |
| Resolve/ignore fails | missing auth/permission | verify token/role and route permissions |
| Fields missing | migration not applied | run alembic upgrade head |
| UI empty | API failure/URL mismatch | inspect network calls and backend logs |

## Handoff

- Submit filled report with defects and repro steps.
- Mark go/no-go based on P0 completion.
