=============================================
SPRINT 5.5 STARTER PACK
=============================================

This is the starter pack for Sprint 5.5 – Expense & Payment Management.

PREREQUISITES:
- Sprint 5.4 completed (Revenue & Commission Processing UI)
- TRN_Expense, TRN_RecurringExpense, TRN_ExpenseClaim, TRN_Payment tables exist
- MST_Vendor, MST_ExpenseCategory, MST_CostCenter tables exist

WHAT YOU WILL BUILD:
- Expense management (operational expenses, recurring expenses, claims)
- Payment management (outbound payments, UTR tracking, bank reconciliation)
- List, create, edit, view, and delete for expenses and payments
- Auto-calculation for recurring expenses

STEPS:
1. Copy ALL files and folders from this pack into your odos project root
2. Follow IMP-5.5.md step by step
3. Start the server and test at http://localhost:8000/masters/expenses

FILES INCLUDED:
- src/masters/api/expense.py      (Expense CRUD + recurring)
- src/masters/api/payment.py      (Payment CRUD + BRS)
- src/masters/ui/routes.py        (UI routes – you will ADD new routes)
- src/templates/masters/*.html    (Expense and Payment list, form, detail)
- scripts/seed_test_expense_payment.py (Optional test data)

ESTIMATED DURATION: 2 days
CONTACT: CTO or Technical Programme Manager
