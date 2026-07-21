=============================================
SPRINT 5.4 STARTER PACK
=============================================

This is the starter pack for Sprint 5.4 – Revenue & Commission Processing.

PREREQUISITES:
- Sprint 5.2 completed (Case Management UI)
- TRN_Revenue, TRN_Commission tables exist
- At least one case exists for testing revenue/commission creation

WHAT YOU WILL BUILD:
- Revenue management (income from lenders)
- Commission management (payouts to connectors)
- Auto-calculation of revenue and commission based on case data
- List, create, edit, view, and delete

STEPS:
1. Copy ALL files and folders from this pack into your odos project root
2. Follow IMP-5.4.md step by step
3. Start the server and test at http://localhost:8000/masters/revenue

FILES INCLUDED:
- src/masters/api/revenue.py      (Revenue CRUD + calculation)
- src/masters/api/commission.py   (Commission CRUD + calculation)
- src/masters/ui/routes.py        (UI routes – you will ADD new routes)
- src/templates/masters/*.html    (Revenue and Commission list, form, detail)
- scripts/seed_test_revenue_commission.py (Optional test data)

ESTIMATED DURATION: 2 days
CONTACT: CTO or Technical Programme Manager
