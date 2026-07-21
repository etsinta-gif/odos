from sqlalchemy.orm import Session

from src.reference.models import (
    REF_BorrowerProfile,
    REF_Channel,
    REF_LoanNature,
    REF_LoanType,
    REF_Location,
    REF_ProductCategory,
    REF_Region,
    REF_Status,
)


REF_MODELS = {
    "REF_LoanType": REF_LoanType,
    "REF_Channel": REF_Channel,
    "REF_ProductCategory": REF_ProductCategory,
    "REF_Status": REF_Status,
    "REF_Region": REF_Region,
    "REF_BorrowerProfile": REF_BorrowerProfile,
    "REF_LoanNature": REF_LoanNature,
    "REF_Location": REF_Location,
}


def resolve_reference(session: Session, table_name: str, code: str | None) -> int | None:
    if code in (None, ""):
        return None
    model = REF_MODELS.get(table_name)
    if model is None:
        raise ValueError(f"Unknown reference table: {table_name}")

    record = session.query(model).filter(model.code == str(code).strip()).first()
    if record is None:
        raise ValueError(f"Reference {table_name} with code '{code}' not found")
    return record.id