# Test Pack 5.1 – Master Data Management (UI & API)

**Document ID:** TEST-5.1  
**Version:** 2.0  
**Status:** Ready for Execution  
**Owner:** Aniket (Testing)  
**Sprint:** 5.1  
**Phase:** Phase 5 – Operational ERP  
**Estimated Duration:** 1 day (test execution)

---

## 1. Test Plan

### 1.1 Scope
- **In-Scope:** CRUD operations and validation for master entities:
  - Customers
  - Lenders
  - Products
  - Employees
  - Connectors
- **Special focus:** FCPL data context for Connectors, Lenders, and Products.
- **Both UI and API** will be tested.
- **Validation:** Data persistence in `MST_*` tables, proper HTTP status codes, UI rendering, and duplicate/PAN validation.
- **Out-of-Scope:** Performance, security penetration, or mobile responsiveness.

### 1.2 Test Environment
- **OS:** Windows / macOS / Linux
- **Browser:** Chrome or Firefox (latest)
- **Server:** FastAPI at `http://localhost:8000`
- **Database:** PostgreSQL or configured DB with MST tables
- **Tools:** Browser, Swagger UI (`/docs`), terminal logs, database query tool

### 1.3 Test Data
- Run `scripts/seed_test_data.py` to populate initial master records.
- Ensure the following real-data fields exist for Connectors:
  - Connector Code
  - PAN
  - GSTIN
  - Bank Name
  - Account Number
  - IFSC
  - Unit Head
- Ensure Lender NBFC flags and Product categories are present.

### 1.4 Test Order
1. Smoke test UI pages.
2. Execute API CRUD for each entity.
3. Execute UI CRUD for each entity.
4. Execute FCPL-specific validation tests.
5. Confirm soft delete and field validations.

### 1.5 Entry Criteria
- IMP-5.1 code deployed and server runs.
- `MST_*` tables exist.
- Initial seed data is available or created manually.

### 1.6 Exit Criteria
- All test cases executed.
- **Pass Rate ≥ 90%**.
- Test Report completed and signed off.

---

## 2. Test Cases

### 2.1 Common Setup
1. Open the `odos` project in VS Code.
2. Open a terminal.
3. Activate the venv:
   ```bash
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate    # Windows
   ```
4. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```
5. Open `http://localhost:8000/docs` and `http://localhost:8000/masters/customers`.

---

### 2.2 API Test Cases

#### TC-API-001: Create Customer via API
| Field | Value |
|-------|-------|
| **Test ID** | TC-API-001 |
| **Feature** | Customer API – POST |
| **Steps** | Use `POST /api/masters/customers` in Swagger. Create a customer with PAN and GSTIN. |
| **Expected Result** | HTTP 201, `customer_id` returned, `is_active=true`. |

#### TC-API-002: Create Lender via API with NBFC flag
| Field | Value |
|-------|-------|
| **Test ID** | TC-API-002 |
| **Feature** | Lender API – POST |
| **Steps** | Use `POST /api/masters/lenders`. Create `Tata Capital` with `is_nbfc=true` and a lender code. |
| **Expected Result** | HTTP 201, lender saved with `is_nbfc=true`. |

#### TC-API-003: Create Product via API with Lender association
| Field | Value |
|-------|-------|
| **Test ID** | TC-API-003 |
| **Feature** | Product API – POST |
| **Steps** | Use `POST /api/masters/products`. Create `Business Loan` linked to a lender. |
| **Expected Result** | HTTP 201, product saved and linked to lender. |

#### TC-API-004: Create Connector via API with full FCPL details
| Field | Value |
|-------|-------|
| **Test ID** | TC-API-004 |
| **Feature** | Connector API – POST |
| **Steps** | Use `POST /api/masters/connectors`. Create a connector with code, PAN, GSTIN, bank details, and unit head. |
| **Expected Result** | HTTP 201, connector appears in response and DB. |

#### TC-API-005: Duplicate PAN validation for Connector
| Field | Value |
|-------|-------|
| **Test ID** | TC-API-005 |
| **Feature** | Connector API – PAN validation |
| **Steps** | Create a connector with an existing PAN. |
| **Expected Result** | HTTP 400 error: duplicate PAN not allowed. |

> Repeat similar API CRUD tests for Customers, Lenders, Products, Employees, and Connectors.

---

### 2.3 UI Test Cases

#### TC-UI-001: Add Connector with Full Details
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-001 |
| **Feature** | Connector Add Page |
| **Steps** | Open `/masters/connectors/add`, fill code, name, PAN, GSTIN, bank details, IFSC, unit head, then save. |
| **Expected Result** | Connector shows on `/masters/connectors` and saves to DB. |

#### TC-UI-002: Add Lender with NBFC flag
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-002 |
| **Feature** | Lender Add Page |
| **Steps** | Open `/masters/lenders/add`, fill lender name, PAN, GSTIN, lender code, set NBFC on. |
| **Expected Result** | Lender saved with `is_nbfc=true`. |

#### TC-UI-003: Add Product with Category
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-003 |
| **Feature** | Product Add Page |
| **Steps** | Open `/masters/products/add`, choose a lender, set `Product Name=Business Loan`, `Product Code=BL-OD`. |
| **Expected Result** | Product saved and linked to lender. |

#### TC-UI-004: Edit Connector details
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-004 |
| **Feature** | Connector Edit Page |
| **Steps** | Edit an existing connector and update bank or unit head details. |
| **Expected Result** | Saved changes reflected in list and DB. |

#### TC-UI-005: Soft delete Connector
| Field | Value |
|-------|-------|
| **Test ID** | TC-UI-005 |
| **Feature** | Connector Delete |
| **Steps** | Delete a connector and verify it disappears from list. |
| **Expected Result** | `is_active=false` in DB and record not shown in lists. |

---

### 2.4 FCPL-Specific Test Cases

#### TC-MDM-001: Create Connector with Full Details
| Field | Value |
|-------|-------|
| **Test ID** | TC-MDM-001 |
| **Feature** | Connector Creation |
| **Steps** | 1. Open `/masters/connectors/add`<br>2. Fill:<br>   - Connector Code: `CON001`<br>   - Connector Name: `DIPALI ANIRUDDHA NEVREKAR`<br>   - PAN: `ABCDE1234F`<br>   - GSTIN: `22ABCDE1234F1Z5`<br>   - Bank Name: `HDFC`<br>   - Account Number: `1234567890`<br>   - IFSC: `HDFC0012345`<br>   - Unit Head: `Sanjay Mehta`<br>3. Click Save |
| **Expected Result** | Connector created and appears in list with full details. |

#### TC-MDM-002: Create Lender with NBFC Flag
| Field | Value |
|-------|-------|
| **Test ID** | TC-MDM-002 |
| **Feature** | Lender Creation |
| **Steps** | 1. Open `/masters/lenders/add`<br>2. Fill:<br>   - Lender Name: `Tata Capital`<br>   - PAN: `TATA1234E`<br>   - GSTIN: `22TATA1234E1Z1`<br>   - Lender Code: `TATA001`<br>   - Is NBFC: `Yes`<br>3. Save |
| **Expected Result** | Lender created with `is_nbfc=true`. |

#### TC-MDM-003: Create Product with Lender Association
| Field | Value |
|-------|-------|
| **Test ID** | TC-MDM-003 |
| **Feature** | Product Creation |
| **Steps** | 1. Ensure a lender exists.<br>2. Open `/masters/products/add`<br>3. Fill:<br>   - Product Name: `Business Loan`<br>   - Product Code: `BL-OD`<br>   - Lender: `Tata Capital`<br>   - Interest Rate: `0.24`<br>   - Min Loan Amount: `100000`<br>   - Max Loan Amount: `5000000`<br>4. Save |
| **Expected Result** | Product created and linked to lender. |

#### TC-MDM-004: PAN Validation (Duplicate Prevention)
| Field | Value |
|-------|-------|
| **Test ID** | TC-MDM-004 |
| **Feature** | Duplicate PAN Validation |
| **Steps** | 1. Create a connector with PAN `ABCDE1234F`.<br>2. Attempt to create another connector with the same PAN.<br>3. Submit. |
| **Expected Result** | HTTP 400 or UI error preventing duplicate PAN. |

#### TC-MDM-005: Connector Hierarchy
| Field | Value |
|-------|-------|
| **Test ID** | TC-MDM-005 |
| **Feature** | Connector Hierarchy |
| **Steps** | 1. Create Connector A (parent).<br>2. Create Connector B and link it to Connector A.<br>3. Verify hierarchy in connector detail or list. |
| **Expected Result** | Parent-child relationship is visible and correct. |

---

## 3. Test Report Template

**Date:** ________________  
**Tester:** Aniket  
**Sprint:** 5.1  

| Category | Test Cases Executed | Passed | Failed | Blocked | Pass Rate (%) |
|----------|---------------------|--------|--------|---------|---------------|
| API Tests | 20 | | | | |
| UI Tests | 20 | | | | |
| FCPL-Specific Tests | 5 | | | | |
| Edge Cases | 3 | | | | |
| **TOTAL** | **48** | | | | | |

**Overall Status:** PASS / FAIL

**Comments:**

---

## 4. Debugging Guide

### Common Issues
- **Server fails to start:** Check terminal for import errors and missing packages.
- **404 on UI pages:** Confirm router inclusion and route prefixes in `src/main.py`.
- **Template errors:** Verify `src/templates/masters` contains the required HTML files and `Jinja2Templates` is configured correctly.
- **Duplicate PAN errors:** Validate PAN uniqueness logic in APIs.
- **Soft delete not working:** Confirm `is_active` is `False` and list endpoints filter on active records.

### Quick verification
- `curl http://localhost:8000/api/masters/customers`
- Verify records in the database using SQL queries.
- Restart the server after any code or template change.

---

## 5. Handoff

After completing tests and filling the Test Report, deliver this pack to the CTO (this chat) for review. Once approved, the CTO will forward it along with the Implementation Pack to Aniket for execution.

**Good luck!**
