import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.transactions.models import TRN_Case, TRN_Commission, TRN_Revenue


def seed_cases(db):
    cases = [
        {
            "case_number": "CASE-1001",
            "customer_id": 1,
            "lender_id": 1,
            "product_id": 1,
            "disbursement_amount": 4000000,
            "sanction_amount": 4200000,
            "current_status": "DISBURSED",
            "is_active": True,
        },
        {
            "case_number": "CASE-1002",
            "customer_id": 2,
            "lender_id": 2,
            "product_id": 2,
            "disbursement_amount": 1200000,
            "sanction_amount": 1300000,
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


def seed_revenue_and_commission(db):
    revenue = db.query(TRN_Revenue).filter(TRN_Revenue.case_id == 1).first()
    if not revenue:
        db.add(
            TRN_Revenue(
                case_id=1,
                revenue_date=date.today(),
                base_revenue_amount=100000.0,
                gst_amount=18000.0,
                tds_amount=10000.0,
                net_amount=108000.0,
                utr_number="UTR1001",
                payment_status="PENDING",
                notes="Seeded revenue",
                is_active=True,
            )
        )
    commission = db.query(TRN_Commission).filter(TRN_Commission.case_id == 1).first()
    if not commission:
        db.add(
            TRN_Commission(
                case_id=1,
                connector_id=1,
                commission_date=date.today(),
                base_commission_amount=54000.0,
                bonus_commission_amount=0.0,
                gross_commission_amount=54000.0,
                gst_amount=9720.0,
                tds_amount=5400.0,
                net_amount=58320.0,
                payment_status="PENDING",
                notes="Seeded commission",
                is_active=True,
            )
        )
    db.commit()
    print("✅ Seeded revenue and commission data")


if __name__ == "__main__":
    db = SessionLocal()
    seed_cases(db)
    seed_revenue_and_commission(db)
    db.close()
