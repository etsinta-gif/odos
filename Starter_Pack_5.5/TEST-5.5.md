# TEST-5.5 Expense & Payment Test Pack

## Overview
This test pack validates the Expense & Payment starter pack for Sprint 5.5. It covers API CRUD, reconciliation, recurring expense templates, and UI workflows.

## 1. Test Data Setup
- Ensure a Case exists with `case_id=1` and a valid `vendor_id`, `expense_category_id`, `cost_center_id`, and `company_bank_account_id`.
- Run `scripts/seed_test_expense_payment.py` if needed.

## 2. API Validation
### Expense
1. `POST /api/masters/expenses/`
   - Payload:
     ```json
     {
       "expense_date": "2025-01-15",
       "vendor_id": 1,
       "expense_category_id": 1,
       "cost_center_id": 1,
       "case_id": 1,
       "description": "Test expense",
       "amount": 15000.0,
       "gst_amount": 2700.0,
       "tds_amount": 1500.0,
       "net_amount": 16200.0,
       "payment_status": "PENDING",
       "invoice_reference": "INV-5001",
       "notes": "Test expense"
     }
     ```
   - Assert status `200` and returned `expense_id`.
2. `GET /api/masters/expenses/{expense_id}`
   - Assert `vendor_name`, `expense_category_name`, `cost_center_name`, and amount fields.
3. `GET /api/masters/expenses/`
   - Assert the created expense appears in the list.
4. `PUT /api/masters/expenses/{expense_id}`
   - Payload: `{ "payment_status": "PAID", "notes": "Updated through API" }`
   - Assert status `200` and updated values.
5. `DELETE /api/masters/expenses/{expense_id}`
   - Assert `is_active` becomes `false` on the record.

### Recurring Expense
1. `POST /api/masters/expenses/recurring`
   - Payload:
     ```json
     {
       "expense_category_id": 1,
       "vendor_id": 1,
       "cost_center_id": 1,
       "description": "Monthly subscription",
       "amount": 12000.0,
       "gst_amount": 2160.0,
       "tds_amount": 1200.0,
       "net_amount": 12960.0,
       "frequency": "MONTHLY",
       "start_date": "2025-01-01",
       "invoice_reference": "INV-REC-5001"
     }
     ```
   - Assert response includes `recurring_expense_id`.
2. `GET /api/masters/expenses/recurring`
   - Assert the recurring template appears in the list.
3. `POST /api/masters/expenses/recurring/generate/{recurring_id}`
   - Assert it creates a new expense record.

### Payment
1. `POST /api/masters/payments/`
   - Payload:
     ```json
     {
       "payment_date": "2025-01-15",
       "company_bank_account_id": 1,
       "payment_amount": 16200.0,
       "payment_mode": "NEFT",
       "utr_number": "UTR-5001",
       "payment_type": "EXPENSE",
       "reference_id": 1,
       "notes": "Payment for expense"
     }
     ```
   - Assert status `200` and returned `payment_id`.
2. `GET /api/masters/payments/{payment_id}`
   - Assert `bank_name`, `payment_type`, and `reconciliation_status`.
3. `GET /api/masters/payments/`
   - Assert the created payment appears in the list.
4. `PUT /api/masters/payments/{payment_id}`
   - Payload: `{ "reconciliation_status": "RECONCILED", "notes": "Updated through API" }`
   - Assert status `200` and updated values.
5. `DELETE /api/masters/payments/{payment_id}`
   - Assert `is_active` becomes `false` on the record.
6. `POST /api/masters/payments/{payment_id}/reconcile`
   - Assert the response confirms reconciliation.
7. `GET /api/masters/payments/reconciliation/pending`
   - Assert only pending payments are returned.

## 3. UI Validation
1. Open `http://localhost:8000/masters/expenses`
   - Assert the page loads and shows expense rows.
2. Add a new expense record through the UI.
3. Open `http://localhost:8000/masters/payments`
   - Assert the page loads and shows payment rows.
4. Add a new payment record through the UI.
5. Edit an expense and a payment record.
6. Reconcile a payment from the UI.

## 4. Edge Cases
- Create expense with an invalid `expense_category_id`: expect `400`.
- Create payment with duplicate `utr_number`: expect `400`.
- Generate expense from a non-existent recurring template: expect `404`.

## 5. Expected Results
- Expense and Payment CRUD functions work in API and UI.
- Recurring expense generation creates a new expense.
- Soft delete sets `is_active=false`.
- Payment reconciliation updates the status.
