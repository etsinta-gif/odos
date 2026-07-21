# Test Pack 5.2 – Case Management (UI & API)

**Document ID:** TEST-5.2  
**Version:** 1.0  
**Status:** Ready for Execution  
**Owner:** Aniket (Testing)  
**Sprint:** 5.2  
**Phase:** Phase 5 – Operational ERP  
**Estimated Duration:** 1 day (test execution)

---

## 1. Test Plan

### 1.1 Scope
- **In-Scope:** Case CRUD and status workflows for `TRN_Case` and `TRN_CaseStatusHistory`.
- **Special focus:** FCPL-specific loan case data, connector splits, payout percentages, processing fee parsing, and tenure parsing.
- **Both UI and API** will be tested.
- **Validation:** Data persistence, status history, correct UI rendering, and parsing of complex case fields.
- **Out-of-Scope:** Performance, security penetration, or mobile responsiveness.

### 1.2 Test Environment
- **OS:** Windows / macOS / Linux
- **Browser:** Chrome or Firefox (latest)
- **Server:** FastAPI at `http://localhost:8000`
- **Database:** PostgreSQL or configured DB with case tables
- **Tools:** Browser, Swagger UI, terminal logs, database query tool

### 1.3 Test Data
- Ensure `MST_Customer`, `MST_Lender`, `MST_Product`, and `MST_Connector` have records.
- Seed sample cases using `scripts/seed_test_cases.py` if available.
- Prepare connector payout splits and lender payout slabs.

### 1.4 Test Order
1. Smoke test case UI pages.
2. Execute case API CRUD.
3. Execute case UI CRUD and detail workflows.
4. Execute FCPL-specific parsing and payout tests.
5. Confirm status history logging.

### 1.5 Entry Criteria
- IMP-5.2 code deployed and server runs.
- Required master data exists.
- Case schema/tables exist.

### 1.6 Exit Criteria
- All test cases completed.
- **Pass Rate ≥ 90%**.
- Test Report completed and signed off.

---

## 2. Test Cases

### 2.1 Common Setup
1. Open `odos` in VS Code.
2. Open a terminal.
3. Activate the virtual environment.
4. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```
5. Open `http://localhost:8000/docs` and `http://localhost:8000/masters/cases`.

---

### 2.2 API Test Cases

#### TC-CASE-001: Create Case via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-001 |
| **Feature** | Create Case |
| **Steps** | Use `POST /api/masters/cases`. Provide customer_id, lender_id, product_id, case_number, status, and financial fields. |
| **Expected Result** | HTTP 201, case created with `case_id`, `status`, and `is_active=true`. |

#### TC-CASE-002: Get Case by ID via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-002 |
| **Feature** | Get Case |
| **Steps** | Use `GET /api/masters/cases/{case_id}` with the created ID. |
| **Expected Result** | HTTP 200, returned case matches saved details. |

#### TC-CASE-003: Update Case via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-003 |
| **Feature** | Update Case |
| **Steps** | Use `PUT /api/masters/cases/{case_id}` to change status, sanction amount, or dates. |
| **Expected Result** | HTTP 200, updated case fields saved. |

#### TC-CASE-004: Soft Delete Case via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-004 |
| **Feature** | Delete Case |
| **Steps** | Use `DELETE /api/masters/cases/{case_id}`. |
| **Expected Result** | HTTP 200, `is_active=false`. Case no longer appears in list endpoint. |

#### TC-CASE-005: Status Transition via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-005 |
| **Feature** | Case Status Transition |
| **Steps** | Use `POST /api/masters/cases/{case_id}/status` with new status values. |
| **Expected Result** | HTTP 200, status updated and history record created. |

---

### 2.3 UI Test Cases

#### TC-UI-CASE-001: View Case List Page
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-CASE-001 |
| **Feature** | Case List Page |
| **Steps** | Open `/masters/cases`. |
| **Expected Result** | Page loads, table displays active cases, and Add Case button is visible. |

#### TC-UI-CASE-002: Add Case via UI
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-CASE-002 |
| **Feature** | Add Case Form |
| **Steps** | Open `/masters/cases/add`, fill required fields, and save. |
| **Expected Result** | Case created and visible in list. |

#### TC-UI-CASE-003: Edit Case via UI
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-CASE-003 |
| **Feature** | Edit Case Form |
| **Steps** | Open `/masters/cases/{case_id}/edit`, change fields, and save. |
| **Expected Result** | Case detail reflects updates. |

#### TC-UI-CASE-004: Delete Case via UI
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-CASE-004 |
| **Feature** | Delete Case |
| **Steps** | Click delete on a case and confirm. |
| **Expected Result** | Case removed from list and `is_active=false` in DB. |

#### TC-UI-CASE-005: Case Detail and Status Transition
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-CASE-005 |
| **Feature** | Case Detail Page |
| **Steps** | Open `/masters/cases/{case_id}` and change status using the form. |
| **Expected Result** | Status updates and history is logged. |

---

### 2.4 FCPL-Specific Test Cases

#### TC-CASE-FCPL-001: Create Case with Connector Split
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-FCPL-001 |
| **Feature** | Case Creation with Connector Split |
| **Prerequisites** | 1 Customer, 1 Lender, 1 Product, 2 Connectors exist. |
| **Steps** | Open `/masters/cases/add` and fill:<br> - customer_id<br> - lender_id<br> - product_id<br> - connector 1 split / percentage<br> - connector 2 split / percentage<br> - application_date<br> - login amount<br> - sanction amount<br> - disbursement amount<br> - interest rate<br> - processing fee `30000(3%)`<br> - tenure `36M`<br> - status `LOGIN DONE - IN PROCESS`<br> Save. |
| **Expected Result** | Case created; processing fee and percentage parsed; tenure stored correctly; connector splits attached. |

#### TC-CASE-FCPL-002: Status Transition Workflow
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-FCPL-002 |
| **Feature** | Status Workflow |
| **Steps** | Create a case with `LOGIN DONE - IN PROCESS`, then transition to `APPROVED`, `SANCTIONED`, `DISBURSED`. |
| **Expected Result** | Each transition updates case status and adds a history row. |

#### TC-CASE-FCPL-003: Processing Fee Parsing
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-FCPL-003 |
| **Feature** | Processing Fee Parsing |
| **Steps** | Create a case with `processing_fee = 30000(3%)` and review stored values. |
| **Expected Result** | Saved as numeric fee and percentage separately (or parsed correctly). |

#### TC-CASE-FCPL-004: Tenure Parsing
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-FCPL-004 |
| **Feature** | Tenure Parsing |
| **Steps** | Create cases with tenures `36M`, `2+4`, `12+36` and verify storage. |
| **Expected Result** | Tenure stored consistently as months. |

#### TC-CASE-FCPL-005: Bank Payout % Display
| Field | Value |
|-------|-------|
| **Test ID** | TC-CASE-FCPL-005 |
| **Feature** | Lender Bank Payout |
| **Steps** | Create a case for a lender with payout slabs; verify payout percentage shown on case detail/list. |
| **Expected Result** | Correct bank payout % based on the configured slab. |

---

## 3. Test Report Template

**Date:** ________________  
**Tester:** Aniket  
**Sprint:** 5.2  

| Category | Test Cases Executed | Passed | Failed | Blocked | Pass Rate (%) |
|----------|---------------------|--------|--------|---------|---------------|
| API Tests | 5 | | | | |
| UI Tests | 5 | | | | |
| FCPL-Specific Tests | 5 | | | | |
| **TOTAL** | **15** | | | | | |

**Overall Status:** PASS / FAIL

**Comments:**

---

## 4. Debugging Guide

- Confirm master records exist before creating cases.
- If case detail page fails, check the case router and template path.
- If status transition does not log history, verify `TRN_CaseStatusHistory` inserts.
- If processing fee parsing fails, review field parsing logic and stored DB fields.

---

## 5. Execution Notes

- Use the UI forms for the main workflow.
- Use Swagger for API validation and error checking.
- Capture screenshots for any failed steps.
