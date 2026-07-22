from types import SimpleNamespace
from uuid import uuid4

from app.main import startup_event
from src.core.database import Base, SessionLocal, engine
from src.etl.handlers.simple import promote_commission_txn, promote_revenue
from src.masters.models import MST_Connector, MST_Lender
from src.transactions.models import ETL_RedFlag, TRN_Case


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def test_promotion_generates_red_flags_and_persists_verification_fields() -> None:
    startup_event()
    db = SessionLocal()
    lender = None
    connector = None
    case = None
    try:
        lender = MST_Lender(
            company_id=1,
            lender_name=f"Lender-{uuid4().hex[:6]}",
            pan=f"ALP{uuid4().hex[:7].upper()}",
            default_gst_rate=18,
            default_tds_rate=2,
            max_commission=10000,
            is_active=True,
        )
        connector = MST_Connector(
            company_id=1,
            connector_code=f"CN{uuid4().hex[:6].upper()}",
            full_name="Connector Test",
            default_gst_rate=18,
            default_tds_rate=5,
            max_commission=2500,
            is_active=True,
        )
        db.add(lender)
        db.add(connector)
        db.commit()
        db.refresh(lender)
        db.refresh(connector)

        case = TRN_Case(
            company_id=1,
            case_number=f"CASE-{uuid4().hex[:8]}",
            customer_id=1,
            lender_id=lender.lender_id,
            product_id=1,
            status="LEAD",
            is_active=True,
        )
        db.add(case)
        db.commit()
        db.refresh(case)

        revenue_rows = [
            {
                "staging_row": SimpleNamespace(company_id=1, batch_guid="intel-promote-batch", staging_id=1),
                "mapped_data": {
                    "company_id": 1,
                    "case_id": case.case_id,
                    "utr_number": f"REV-{uuid4().hex[:10]}",
                    "reported_amount": 1000,
                    "reported_gst": 10,
                    "reported_tds": 0,
                    "net_amount": 990,
                },
            }
        ]
        rev_result = promote_revenue(db, revenue_rows, template=None, conflict_resolution="SKIP")
        assert rev_result["created"] >= 1
        assert rev_result.get("red_flags", 0) >= 1

        commission_rows = [
            {
                "staging_row": SimpleNamespace(company_id=1, batch_guid="intel-promote-batch", staging_id=2),
                "mapped_data": {
                    "company_id": 1,
                    "case_id": case.case_id,
                    "connector_id": connector.connector_id,
                    "utr_number": f"COM-{uuid4().hex[:10]}",
                    "reported_commission": 3000,
                    "reported_gst": 540,
                    "reported_tds": 150,
                    "net_amount": 2310,
                },
            }
        ]
        com_result = promote_commission_txn(db, commission_rows, template=None, conflict_resolution="SKIP")
        assert com_result["created"] >= 1
        assert com_result.get("red_flags", 0) >= 1

        flags = db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "intel-promote-batch").all()
        assert len(flags) >= 2
    finally:
        db.query(ETL_RedFlag).filter(ETL_RedFlag.batch_guid == "intel-promote-batch").delete()
        if case is not None:
            db.query(TRN_Case).filter(TRN_Case.case_id == case.case_id).delete()
        if connector is not None:
            db.query(MST_Connector).filter(MST_Connector.connector_id == connector.connector_id).delete()
        if lender is not None:
            db.query(MST_Lender).filter(MST_Lender.lender_id == lender.lender_id).delete()
        db.commit()
        db.close()
