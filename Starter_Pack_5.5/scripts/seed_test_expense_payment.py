import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.transactions.models import TRN_Case, TRN_Expense, TRN_RecurringExpense, TRN_Payment


def seed_cases(db):
    cases = [
        {
            "case_number": "CASE-2001",
            "customer_id": 1,
            "lender_id": 1,
            "product_id": 1,
            "disbursement_amount": 2500000,
            "sanction_amount": 2600000,
            "current_status": "DISBURSED",
            "is_active": True,
        },
        {
            "case_number": "CASE-2002",
            "customer_id": 2,
            "lender_id": 2,
            "product_id": 2,
            "disbursement_amount": 1800000,
            "sanction_amount": 1900000,
            "current_status": "DISBURSED",
            "is_active": True,
        },
    ]
    for data in cases:
        existing = db.query(TRN_Case).filter(TRN_Case.case_number == data["case_number"]).first()
        if not existing:
            db.add(TRN_Case(**data))
    db.commit()
    print("✅ Seeded case data")


def seed_expenses_and_payments(db):
    expense = db.query(TRN_Expense).filter(TRN_Expense.description == "Seeded operating expense").first()
    if not expense:
        db.add(
            TRN_Expense(
                expense_date=date.today(),
                vendor_id=1,
                expense_category_id=1,
                cost_center_id=1,
                case_id=1,
                description="Seeded operating expense",
                amount=15000.0,
                gst_amount=2700.0,
                tds_amount=1500.0,
                net_amount=16200.0,
                payment_status="PENDING",
                invoice_reference="INV-2001",
                notes="Seeded expense record",
                is_active=True,
            )
        )
    recurring = db.query(TRN_RecurringExpense).filter(TRN_RecurringExpense.description == "Seeded recurring expense").first()
    if not recurring:
        db.add(
            TRN_RecurringExpense(
                expense_category_id=1,
                vendor_id=1,
                cost_center_id=1,
                description="Seeded recurring expense",
                amount=12000.0,
                gst_amount=2160.0,
                tds_amount=1200.0,
                net_amount=12960.0,
                frequency="MONTHLY",
                start_date=date.today(),
                end_date=None,
                invoice_reference="INV-REC-2001",
                notes="Seeded recurring expense template",
                is_active=True,
            )
        )
    payment = db.query(TRN_Payment).filter(TRN_Payment.reference_id == 1).first()
    if not payment:
        db.add(
            TRN_Payment(
                payment_number="PAY-2001",
                payment_date=date.today(),
                company_bank_account_id=1,
                payment_amount=16200.0,
                payment_mode="NEFT",
                utr_number="UTR-2001",
                payment_type="EXPENSE",
                reference_id=1,
                reconciliation_status="PENDING",
                notes="Seeded payment for expense",
                is_active=True,
            )
        )
    db.commit()
    print("✅ Seeded expense and payment data")


if __name__ == "__main__":
    db = SessionLocal()
    seed_cases(db)
    seed_expenses_and_payments(db)
    db.close()
