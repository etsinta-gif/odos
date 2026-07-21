# src/etl/services/duplicate_detector.py
from sqlalchemy.orm import Session
from src.transactions.models import TRN_Case  # example target table

def check_duplicates(db: Session, company_id: int, row: dict, key_fields: list) -> bool:
    """Return True if a record with same key_fields exists in target table."""
    query = db.query(TRN_Case).filter(TRN_Case.company_id == company_id)
    for field in key_fields:
        value = row.get(field)
        if value is not None:
            query = query.filter(getattr(TRN_Case, field) == value)
    return query.first() is not None
