# src/etl/services/lineage.py
from sqlalchemy.orm import Session
from src.etl.models import ETL_DataLineage
from datetime import datetime

def capture_lineage(db: Session, batch_guid: str, company_id: int, source_system: str,
                    source_file: str, source_row: int, target_table: str, target_record_id: int):
    lineage = ETL_DataLineage(
        batch_guid=batch_guid,
        company_id=company_id,
        source_system=source_system,
        source_file=source_file,
        source_row=source_row,
        target_table=target_table,
        target_record_id=target_record_id,
        transformation_log="mapped and validated",
        created_at=datetime.utcnow()
    )
    db.add(lineage)
    db.commit()
