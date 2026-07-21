# src/etl/services/transformer.py
from sqlalchemy.orm import Session
from src.etl.services.mapper import get_mappings, apply_mapping
from src.metadata.models import META_FieldDefinition
from datetime import datetime
import re

def convert_type(value, logical_type: str):
    """Convert value to the appropriate Python type based on logical_type."""
    if value is None or value == "":
        return None
    logical_type = logical_type.lower()
    if "date" in logical_type:
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(value, fmt).date()
            except (ValueError, TypeError):
                continue
        return None
    if "decimal" in logical_type or "amount" in logical_type or "numeric" in logical_type:
        cleaned = re.sub(r'[^\d.]', '', str(value))
        try:
            return float(cleaned)
        except ValueError:
            return None
    if "integer" in logical_type:
        try:
            return int(value)
        except ValueError:
            return None
    if "boolean" in logical_type:
        return str(value).lower() in ("yes", "true", "1", "y")
    return str(value)


def transform_raw_data(db: Session, company_id: int, source_system: str, raw_rows: list) -> list:
    """
    For each raw row, apply mapping and type conversion.
    Returns list of transformed dicts with canonical field names and converted values.
    """
    mappings = get_mappings(db, company_id, source_system)
    field_defs = db.query(META_FieldDefinition).filter(
        META_FieldDefinition.company_id == company_id
    ).all()
    field_type_map = {f.field_name: f.logical_data_type for f in field_defs}

    transformed_rows = []
    for raw in raw_rows:
        mapped = apply_mapping(raw, mappings)
        converted = {}
        for field, value in mapped.items():
            logical_type = field_type_map.get(field, "text")
            converted[field] = convert_type(value, logical_type)
        transformed_rows.append(converted)
    return transformed_rows
