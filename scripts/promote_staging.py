import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import SessionLocal
from src.etl.services.promoter import promote_batch
from src.transactions.models import ETL_ImportBatch


def promote_staging(batch_guid: str | None = None, conflict_resolution: str = "SKIP") -> None:
    db = SessionLocal()
    try:
        policy = (conflict_resolution or "SKIP").upper()
        if batch_guid:
            result = promote_batch(db, batch_guid, policy)
            if result.get("error"):
                print(f"Error: {result['error']}")
            else:
                print(f"Promotion complete for {batch_guid}: {result.get('results', {})}")
            return

        batches = (
            db.query(ETL_ImportBatch)
            .filter(ETL_ImportBatch.import_status == "STAGED")
            .filter(ETL_ImportBatch.is_complete == False)
            .order_by(ETL_ImportBatch.import_datetime.asc())
            .all()
        )
        if not batches:
            print("No pending batches to promote.")
            return

        for batch in batches:
            result = promote_batch(db, batch.batch_guid, policy)
            if result.get("error"):
                print(f"Error promoting {batch.batch_guid}: {result['error']}")
            else:
                print(f"Promotion complete for {batch.batch_guid}: {result.get('results', {})}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Promote validated ETL records")
    parser.add_argument("--batch-guid", dest="batch_guid", default=None)
    parser.add_argument("--conflict-resolution", dest="conflict_resolution", default="SKIP")
    args = parser.parse_args()
    promote_staging(batch_guid=args.batch_guid, conflict_resolution=args.conflict_resolution)
