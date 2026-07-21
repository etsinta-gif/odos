# src/etl/services/mapper.py
from sqlalchemy.orm import Session
from src.metadata.models import META_FieldMapping, META_FieldDefinition

def get_mappings(db: Session, company_id: int, source_system: str):
    """Fetch all active mappings for a given source system."""
    mappings = db.query(META_FieldMapping).filter(
        META_FieldMapping.company_id == company_id,
        META_FieldMapping.source_system == source_system,
        META_FieldMapping.is_verified == True
    ).all()
    mapping_dict = {}
    for m in mappings:
        target_field = db.query(META_FieldDefinition).filter_by(field_def_id=m.field_def_id).first()
        if target_field:
            mapping_dict[m.source_header] = target_field.field_name
    return mapping_dict


def apply_mapping(raw_row: dict, mapping_dict: dict) -> dict:
    """Transform a raw row using the mapping dict."""
    transformed = {}
    for source_col, value in raw_row.items():
        if source_col in mapping_dict:
            transformed[mapping_dict[source_col]] = value
    return transformed
