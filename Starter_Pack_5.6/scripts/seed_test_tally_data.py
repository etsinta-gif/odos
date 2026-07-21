import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.transactions.models import TRN_TallyExportBatch, TRN_TallyExportDetail


def seed_tally_data(db):
    batches = [
        {
            "batch_name": "April 2026 Tally Export",
            "batch_number": "TALLY-20260430-001",
            "export_type": "ALL",
            "period_start": date(2026, 4, 1),
            "period_end": date(2026, 4, 30),
            "total_records": 4,
            "exported_records": 4,
            "export_status": "COMPLETED",
            "sync_status": "SYNCED",
            "notes": "Full April export",
            "is_active": True,
        },
        {
            "batch_name": "May 2026 Revenue Export",
            "batch_number": "TALLY-20260531-001",
            "export_type": "REVENUE",
            "period_start": date(2026, 5, 1),
            "period_end": date(2026, 5, 31),
            "total_records": 0,
            "exported_records": 0,
            "export_status": "PENDING",
            "sync_status": "PENDING",
            "notes": "Revenue only batch",
            "is_active": True,
        },
    ]

    for batch_data in batches:
        existing = db.query(TRN_TallyExportBatch).filter(
            TRN_TallyExportBatch.batch_number == batch_data["batch_number"]
        ).first()
        if not existing:
            batch = TRN_TallyExportBatch(**batch_data)
            db.add(batch)
            db.flush()

            if batch.export_status == "COMPLETED":
                details = [
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "REVENUE",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-15",
                            "amount": 45000.0,
                            "case_id": 1,
                            "gst": 8100.0,
                            "tds": 4500.0,
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "COMMISSION",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-20",
                            "amount": 13500.0,
                            "case_id": 1,
                            "connector_id": 1,
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "EXPENSE",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-01",
                            "amount": 54000.0,
                            "category": 1,
                            "description": "Office rent April 2026",
                        }),
                        "export_status": "COMPLETED",
                    },
                    {
                        "batch_id": batch.batch_id,
                        "source_table": "PAYMENT",
                        "source_id": 1,
                        "exported_data": json.dumps({
                            "date": "2026-04-01",
                            "amount": 54000.0,
                            "mode": "NEFT",
                            "utr": "UTR-20260401001",
                        }),
                        "export_status": "COMPLETED",
                    },
                ]
                for detail_data in details:
                    detail = TRN_TallyExportDetail(**detail_data)
                    db.add(detail)

    db.commit()
    print("✅ Seeded tally export batches and details")


if __name__ == "__main__":
    db = SessionLocal()
    seed_tally_data(db)
    db.close()
