# src/etl/services/loader.py
from sqlalchemy.orm import Session
from src.masters.models import MST_Customer, MST_Company
from src.transactions.models import TRN_Case


def load_data(db: Session, company_id: int, rows: list, target_table: str) -> int:
    """
    Insert rows into the specified target table.
    Returns number of rows inserted.
    """
    model_map = {
        "MST_Customer": MST_Customer,
        "TRN_Case": TRN_Case,
    }
    model = model_map.get(target_table)
    if not model:
        raise ValueError(f"Unknown target table: {target_table}")
    inserted = 0
    for row in rows:
        row["company_id"] = company_id
        new_record = model(**row)
        db.add(new_record)
        inserted += 1
    db.commit()
    return inserted
