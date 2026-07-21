import json
from datetime import datetime

from sqlalchemy.orm import Session

from src.metadata.models import META_FieldMapping, META_ImportTemplate

VALID_STATUS_TRANSITIONS = {
    "Draft": {"Approved", "Deprecated", "Deleted"},
    "Approved": {"Active", "Deprecated", "Deleted"},
    "Active": {"Deprecated", "Deleted"},
    "Deprecated": {"Draft", "Deleted"},
    "Deleted": set(),
}


def _append_history(template: META_ImportTemplate, action: str) -> None:
    try:
        history = json.loads(template.mapping_definition_history or "[]")
    except Exception:
        history = []

    history.append(
        {
            "action": action,
            "version": template.version,
            "status": template.status,
            "conflict_resolution": template.conflict_resolution,
            "mapping_definition": template.mapping_definition,
            "updated_by": template.updated_by,
            "updated_at": datetime.utcnow().isoformat(),
        }
    )
    template.mapping_definition_history = json.dumps(history[-10:])


def _ensure_status_transition(current: str, target: str) -> None:
    if target == current:
        return
    allowed = VALID_STATUS_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise ValueError(f"Invalid status transition from {current} to {target}")


def create_template(db: Session, template_data: dict) -> META_ImportTemplate:
    template = META_ImportTemplate(
        template_name=template_data["template_name"],
        file_pattern=template_data.get("file_pattern"),
        fingerprint=template_data.get("fingerprint"),
        sheet_name=template_data.get("sheet_name", "Sheet1"),
        header_row=template_data.get("header_row", 1),
        version=max(int(template_data.get("version", 1)), 1),
        status=template_data.get("status", "Draft"),
        conflict_resolution=str(template_data.get("conflict_resolution", "SKIP")).upper(),
        shared=bool(template_data.get("shared", False)),
        company_id=template_data.get("company_id"),
        is_active=True,
        created_by="admin",
        created_at=datetime.utcnow(),
        updated_by="admin",
        updated_at=datetime.utcnow(),
    )
    db.add(template)
    db.flush()

    mappings = template_data.get("mappings", [])
    for mapping in mappings:
        field_mapping = META_FieldMapping(
            template_id=template.template_id,
            company_id=template.company_id,
            source_column=mapping["source_column"],
            target_table=mapping["target_table"],
            target_field=mapping["target_field"],
            confidence_score=mapping.get("confidence_score", 0),
            is_verified=mapping.get("is_verified", False),
            is_natural_key=mapping.get("is_natural_key", False),
            transformation_rule=mapping.get("transformation_rule"),
            notes=mapping.get("notes"),
        )
        db.add(field_mapping)

    mapping_json = {
        "sheet_name": template.sheet_name,
        "header_row": template.header_row,
        "mappings": mappings,
        "conflict_resolution": template.conflict_resolution,
    }
    template.mapping_definition = json.dumps(mapping_json)
    template.mapping_definition_history = json.dumps([])

    db.commit()
    db.refresh(template)
    return template


def get_template(db: Session, template_id: int) -> META_ImportTemplate | None:
    return (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.template_id == template_id)
        .filter(META_ImportTemplate.status != "Deleted")
        .first()
    )


def list_templates(db: Session) -> list[META_ImportTemplate]:
    return db.query(META_ImportTemplate).filter(META_ImportTemplate.status != "Deleted").all()


def list_templates_scoped(db: Session, company_id: int) -> list[META_ImportTemplate]:
    return (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.status != "Deleted")
        .filter((META_ImportTemplate.shared == True) | (META_ImportTemplate.company_id == company_id))
        .all()
    )


def update_template(db: Session, template_id: int, template_data: dict) -> META_ImportTemplate | None:
    template = get_template(db, template_id)
    if not template:
        return None

    _append_history(template, action="update")
    template.version += 1

    if "template_name" in template_data:
        template.template_name = template_data["template_name"]
    if "file_pattern" in template_data:
        template.file_pattern = template_data["file_pattern"]
    if "fingerprint" in template_data:
        template.fingerprint = template_data["fingerprint"]
    if "conflict_resolution" in template_data and template_data["conflict_resolution"]:
        template.conflict_resolution = str(template_data["conflict_resolution"]).upper()
    if "status" in template_data:
        target_status = str(template_data["status"])
        _ensure_status_transition(template.status, target_status)
        template.status = target_status
        template.is_active = template.status != "Deleted"

    if "mappings" in template_data:
        db.query(META_FieldMapping).filter(META_FieldMapping.template_id == template_id).delete()
        for mapping in template_data["mappings"]:
            db.add(
                META_FieldMapping(
                    template_id=template_id,
                    company_id=template.company_id,
                    source_column=mapping["source_column"],
                    target_table=mapping["target_table"],
                    target_field=mapping["target_field"],
                    confidence_score=mapping.get("confidence_score", 0),
                    is_verified=mapping.get("is_verified", False),
                    is_natural_key=mapping.get("is_natural_key", False),
                    transformation_rule=mapping.get("transformation_rule"),
                    notes=mapping.get("notes"),
                )
            )
        template.mapping_definition = json.dumps(
            {
                "sheet_name": template.sheet_name,
                "header_row": template.header_row,
                "mappings": template_data["mappings"],
                "conflict_resolution": template.conflict_resolution,
            }
        )

    template.updated_by = "admin"
    template.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(template)
    return template


def delete_template(db: Session, template_id: int) -> bool:
    template = get_template(db, template_id)
    if not template:
        return False
    _append_history(template, action="delete")
    template.version += 1
    template.status = "Deleted"
    template.is_active = False
    template.updated_by = "admin"
    template.updated_at = datetime.utcnow()
    db.commit()
    return True
