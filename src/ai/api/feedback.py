from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.ai.services.feedback import record_learning_event, record_mapping_feedback
from src.core.database import get_db

router = APIRouter(prefix="/api/ai/feedback", tags=["AI"])


class MappingFeedbackIn(BaseModel):
    metadata_id: int | None = None
    template_id: int | None = None
    batch_guid: str | None = None
    sheet_name: str | None = None
    source_column: str | None = None
    target_table: str | None = None
    target_field: str | None = None
    confidence_score: int | None = None
    confidence_level: str | None = None
    formula_detected: bool = False
    formula_status: str | None = None
    user_decision: str = "APPROVED"
    discrepancy_reason: str | None = None
    payload: dict | None = None


class LearningEventIn(BaseModel):
    metadata_id: int | None = None
    mapping_id: int | None = None
    event_type: str
    payload: dict | None = None
    model_name: str | None = None
    model_version: str | None = None
    confidence_before: float | None = None
    confidence_after: float | None = None


@router.post("/mapping")
def create_mapping_feedback(payload: MappingFeedbackIn, db: Session = Depends(get_db)):
    try:
        feedback = record_mapping_feedback(db, **payload.model_dump())
        db.commit()
        return {"feedback_id": feedback.feedback_id, "status": "stored"}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/learning")
def create_learning_event(payload: LearningEventIn, db: Session = Depends(get_db)):
    try:
        event = record_learning_event(db, **payload.model_dump())
        db.commit()
        return {"learning_id": event.learning_id, "status": "stored"}
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
