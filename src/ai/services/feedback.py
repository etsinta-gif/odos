import json
from typing import Any

from sqlalchemy.orm import Session

from src.ai.models import AI_Feedback, AI_Learning, AI_Mapping, AI_Metadata


def create_ai_metadata(
    db: Session,
    *,
    file_name: str,
    file_hash: str,
    source_system: str | None = None,
    sheet_name: str | None = None,
    header_columns: list[str] | None = None,
    data_types: dict[str, Any] | None = None,
    row_count: int | None = None,
    import_batch_guid: str | None = None,
    confidence: float | None = None,
    company_id: int | None = 1,
) -> AI_Metadata:
    existing = db.query(AI_Metadata).filter(AI_Metadata.file_hash == file_hash).first()
    if existing:
        return existing

    metadata = AI_Metadata(
        company_id=company_id,
        source_system=source_system,
        file_name=file_name,
        file_hash=file_hash,
        sheet_name=sheet_name,
        header_columns=json.dumps(header_columns or []),
        data_types=json.dumps(data_types or {}),
        row_count=row_count,
        import_batch_guid=import_batch_guid,
        confidence=confidence,
    )
    db.add(metadata)
    db.flush()
    return metadata


def record_mapping_feedback(
    db: Session,
    *,
    metadata_id: int | None,
    template_id: int | None,
    batch_guid: str | None,
    sheet_name: str | None,
    source_column: str | None,
    target_table: str | None,
    target_field: str | None,
    confidence_score: int | None,
    confidence_level: str | None,
    formula_detected: bool = False,
    formula_status: str | None = None,
    user_decision: str = "APPROVED",
    discrepancy_reason: str | None = None,
    payload: dict[str, Any] | None = None,
) -> AI_Feedback:
    feedback = AI_Feedback(
        metadata_id=metadata_id,
        template_id=template_id,
        batch_guid=batch_guid,
        sheet_name=sheet_name,
        source_column=source_column,
        target_table=target_table,
        target_field=target_field,
        confidence_score=confidence_score,
        confidence_level=confidence_level,
        formula_detected=formula_detected,
        formula_status=formula_status,
        user_decision=user_decision,
        discrepancy_reason=discrepancy_reason,
        feedback_payload=json.dumps(payload or {}, default=str),
    )
    db.add(feedback)
    db.flush()
    return feedback


def record_learning_event(
    db: Session,
    *,
    metadata_id: int | None,
    mapping_id: int | None,
    event_type: str,
    payload: dict[str, Any] | None = None,
    model_name: str | None = None,
    model_version: str | None = None,
    confidence_before: float | None = None,
    confidence_after: float | None = None,
) -> AI_Learning:
    event = AI_Learning(
        metadata_id=metadata_id,
        mapping_id=mapping_id,
        event_type=event_type,
        event_payload=json.dumps(payload or {}, default=str),
        model_name=model_name,
        model_version=model_version,
        confidence_before=confidence_before,
        confidence_after=confidence_after,
    )
    db.add(event)
    db.flush()
    return event


def record_mapping_snapshot(
    db: Session,
    *,
    metadata_id: int | None,
    source_column: str,
    target_table: str,
    target_field: str,
    confidence: float | None,
    is_verified: bool,
    notes: str | None = None,
) -> AI_Mapping:
    mapping = AI_Mapping(
        metadata_id=metadata_id,
        source_column=source_column,
        target_table=target_table,
        target_field=target_field,
        confidence=confidence,
        is_verified=is_verified,
        notes=notes,
    )
    db.add(mapping)
    db.flush()
    return mapping
