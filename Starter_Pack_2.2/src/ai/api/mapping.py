# src/ai/api/mapping.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.ai.services.mapping_suggester import suggest_mappings
from src.ai.services.mapping_validator import validate_mapping_suggestion
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/ai/mapping", tags=["AI"])

class MappingRequest(BaseModel):
    source_columns: List[str]
    company_id: int
    min_confidence: float = 0.5

class MappingResponse(BaseModel):
    source_column: str
    target_field_id: int
    target_field_name: str
    confidence: float
    is_valid: bool

@router.post("/suggest", response_model=List[MappingResponse])
def suggest_mappings_endpoint(request: MappingRequest, db: Session = Depends(get_db)):
    suggestions = suggest_mappings(db, request.company_id, request.source_columns)
    result = []
    for s in suggestions:
        valid = validate_mapping_suggestion(s, request.min_confidence)
        result.append({
            "source_column": s["source_column"],
            "target_field_id": s["target_field_id"],
            "target_field_name": s["target_field_name"],
            "confidence": s["confidence"],
            "is_valid": valid
        })
    return result
