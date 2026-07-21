# TEST-5.4 Revenue & Commission Test Pack

## Overview
This test pack validates the Revenue & Commission starter pack for Sprint 5.4. It covers API CRUD, calculation helpers, and UI workflows for revenue and commission entry.

## 1. Test Data Setup
- Ensure a Case exists with `case_id=1` and a valid `lender_id`.
- Ensure a Connector exists with `connector_id=1`.
- Run `scripts/seed_test_revenue_commission.py` if needed.

## 2. API Validation
### Revenue
1. `POST /api/masters/revenue/`
   - Payload: `{ "case_id": 1, "revenue_date": "2025-01-15", "base_revenue_amount": 100000.0, "gst_amount": 18000.0, "tds_amount": 10000.0, "net_amount": 108000.0, "payment_status": "PENDING", "notes": "Test revenue" }`
   - Assert status `200` and returned `revenue_id`.
2. `GET /api/masters/revenue/1`
   - Assert `case_id`, `case_number`, `lender_name`, and amount fields.
3. `GET /api/masters/revenue/`
   - Assert the created revenue appears in the list.
4. `PUT /api/masters/revenue/1`
   - Payload: `{ "payment_status": "PAID", "notes": "Updated through API" }`
   - Assert status `200` and updated values.
5. `DELETE /api/masters/revenue/1`
   - Assert `is_active` becomes `false` on the record.

### Commission
1. `POST /api/masters/commission/`
   - Payload: `{ "case_id": 1, "connector_id": 1, "commission_date": "2025-01-15", "base_commission_amount": 50000.0, "bonus_commission_amount": 0.0, "gross_commission_amount": 50000.0, "gst_amount": 9000.0, "tds_amount": 5000.0, "net_amount": 54000.0, "payment_status": "PENDING", "notes": "Test commission" }`
   - Assert status `200` and returned `commission_id`.
2. `GET /api/masters/commission/1`
   - Assert `case_number`, `connector_name`, and amount fields.
3. `GET /api/masters/commission/`
   - Assert the created commission appears in the list.
4. `PUT /api/masters/commission/1`
   - Payload: `{ "payment_status": "PAID", "notes": "Updated through API" }`
   - Assert status `200` and updated values.
5. `DELETE /api/masters/commission/1`
   - Assert `is_active` becomes `false` on the record.

## 3. Calculation API Validation
1. `POST /api/masters/revenue/calculate/1`
   - Assert response includes `base_revenue`, `gst_amount`, `tds_amount`, and `net_amount`.
2. `POST /api/masters/commission/calculate/1`
   - Assert response includes `base_commission`, `gst_amount`, `tds_amount`, and `net_amount`.
   - If revenue is missing for the case, assert an error message.

## 4. UI Validation
1. Open `http://localhost:8000/masters/revenue`
   - Assert the page loads and shows revenue rows.
2. Add a new revenue record using the UI.
   - Assert the form submits and saves successfully.
3. Open `http://localhost:8000/masters/commission`
   - Assert the page loads and shows commission rows.
4. Add a new commission record using the UI.
   - Assert the form submits and saves successfully.
5. Edit a revenue and a commission record.
   - Assert changes persist.

## 5. Edge Cases
- Create revenue with an invalid `case_id`: expect `400`.
- Create commission with invalid `connector_id`: expect `400`.
- Calculate commission when revenue is missing: expect user-friendly error.

## 6. Expected Results
- Revenue and Commission CRUD functions complete successfully.
- Calculation helpers return consistent derived amounts.
- UI pages render lists and forms without server errors.
- Soft delete sets `is_active=false` while preserving records.
