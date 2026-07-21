# scripts/seed_test_cases.py
from src.core.database import get_db
from src.transactions.models import TRN_Case, TRN_CaseStatusHistory
from src.masters.models import MST_Customer, MST_Lender, MST_Product
from datetime import date, datetime


def seed_cases():
    db = next(get_db())

    customer = db.query(MST_Customer).filter(MST_Customer.is_active == True).first()
    lender = db.query(MST_Lender).filter(MST_Lender.is_active == True).first()
    product = db.query(MST_Product).filter(MST_Product.is_active == True).first()

    if not customer or not lender or not product:
        print("Please seed master customer, lender, and product records before running this script.")
        return

    cases = [
        TRN_Case(
            case_number="FY24-25/SC/0001",
            customer_id=customer.customer_id,
            lender_id=lender.lender_id,
            product_id=product.product_id,
            application_date=date(2024, 4, 1),
            sanction_date=None,
            disbursement_date=None,
            sanction_amount=None,
            disbursement_amount=None,
            status="LEAD",
            is_active=True
        ),
        TRN_Case(
            case_number="FY24-25/SC/0002",
            customer_id=customer.customer_id,
            lender_id=lender.lender_id,
            product_id=product.product_id,
            application_date=date(2024, 4, 5),
            sanction_date=date(2024, 4, 12),
            disbursement_date=None,
            sanction_amount=500000.00,
            disbursement_amount=None,
            status="APPLICATION",
            is_active=True
        )
    ]

    for case in cases:
        db.add(case)
    db.commit()

    for case in cases:
        db.add(TRN_CaseStatusHistory(
            case_id=case.case_id,
            status=case.status,
            changed_at=datetime.utcnow()
        ))
    db.commit()

    print("Seeded sample cases.")


if __name__ == "__main__":
    seed_cases()
