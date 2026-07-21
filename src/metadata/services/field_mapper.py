import json
import re
from typing import Any, Optional

from sqlalchemy.orm import Session

from src.metadata.models import META_FieldMapping, META_ImportTemplate


def _scope_query(query, company_id: Optional[int]):
    if company_id is None:
        return query
    return query.filter((META_ImportTemplate.company_id == company_id) | (META_ImportTemplate.shared == True))


def get_template_by_fingerprint(db: Session, fingerprint: str, company_id: Optional[int] = None) -> Optional[META_ImportTemplate]:
    query = (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.fingerprint == fingerprint)
        .filter(META_ImportTemplate.status == "Active")
        .filter(META_ImportTemplate.is_active == True)
    )
    query = _scope_query(query, company_id)
    return query.order_by(META_ImportTemplate.version.desc(), META_ImportTemplate.template_id.desc()).first()


def get_template_by_pattern(db: Session, file_name: str, company_id: Optional[int] = None) -> Optional[META_ImportTemplate]:
    query = (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.status == "Active")
        .filter(META_ImportTemplate.is_active == True)
    )
    query = _scope_query(query, company_id)
    templates = query.order_by(META_ImportTemplate.version.desc(), META_ImportTemplate.template_id.desc()).all()
    for template in templates:
        if not template.file_pattern:
            continue

        candidates = [template.file_pattern]
        # Some stored patterns are double-escaped (e.g. "\\\\.xlsx"); try normalized variant too.
        if "\\\\" in template.file_pattern:
            candidates.append(template.file_pattern.replace("\\\\", "\\"))

        for pattern in candidates:
            try:
                if re.search(pattern, file_name, re.IGNORECASE):
                    return template
            except re.error:
                continue
    return None


def get_template_by_name(db: Session, template_name: str, company_id: Optional[int] = None) -> Optional[META_ImportTemplate]:
    query = (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.template_name == template_name)
        .filter(META_ImportTemplate.status == "Active")
        .filter(META_ImportTemplate.is_active == True)
    )
    query = _scope_query(query, company_id)
    return query.order_by(META_ImportTemplate.version.desc(), META_ImportTemplate.template_id.desc()).first()


def list_templates(db: Session, company_id: int) -> list[META_ImportTemplate]:
    return (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.status == "Active")
        .filter(META_ImportTemplate.is_active == True)
        .filter((META_ImportTemplate.company_id == company_id) | (META_ImportTemplate.shared == True))
        .order_by(META_ImportTemplate.version.desc(), META_ImportTemplate.template_id.desc())
        .all()
    )


def get_template_mappings(db: Session, template_id: int) -> dict[str, Any]:
    mappings = db.query(META_FieldMapping).filter(META_FieldMapping.template_id == template_id).all()
    result: dict[str, Any] = {}
    for mapping in mappings:
        result[mapping.source_column] = {
            "target_table": mapping.target_table,
            "target_field": mapping.target_field,
            "transformation_rule": mapping.transformation_rule,
        }
    return result


def get_mapping_for_etl(db: Session, template_id: int) -> dict[str, Any]:
    template = db.query(META_ImportTemplate).filter(META_ImportTemplate.template_id == template_id).first()
    if not template or not template.mapping_definition:
        return {}
    try:
        return json.loads(template.mapping_definition)
    except Exception:
        return {}
