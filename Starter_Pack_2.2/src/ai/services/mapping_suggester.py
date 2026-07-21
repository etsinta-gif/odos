# src/ai/services/mapping_suggester.py
import re
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.metadata.models import META_FieldDefinition
from src.ai.models import AI_Metadata

def suggest_mappings(db: Session, company_id: int, source_columns: List[str]) -> List[Dict[str, Any]]:
    """
    For each source column, suggest a target field from META_FieldDefinition.
    Returns a list of dicts with 'source_column', 'target_field', 'confidence'.
    """
    fields = db.query(META_FieldDefinition).filter(
        META_FieldDefinition.company_id == company_id,
        META_FieldDefinition.is_active == True
    ).all()

    suggestions = []
    for col in source_columns:
        best_match = None
        best_score = 0.0
        for field in fields:
            score = calculate_similarity(col, field.field_name, field.friendly_name, field.business_definition)
            if score > best_score:
                best_score = score
                best_match = field
        if best_match and best_score > 0.3:
            suggestions.append({
                "source_column": col,
                "target_field_id": best_match.field_def_id,
                "target_field_name": best_match.field_name,
                "confidence": best_score
            })
    return suggestions

def calculate_similarity(source: str, field_name: str, friendly_name: str, business_def: str) -> float:
    """Simple heuristic: exact matches, partial matches, synonyms."""
    source_lower = source.lower()
    if source_lower == field_name.lower() or source_lower == friendly_name.lower():
        return 1.0
    if source_lower in friendly_name.lower() or source_lower in business_def.lower():
        return 0.8
    synonyms = {
        "customer": ["borrower", "client", "applicant"],
        "pan": ["permanent account number", "pan card"],
        "amount": ["loan amount", "disbursement", "principal"],
        "date": ["dt", "date of", "timestamp"],
    }
    for key, syns in synonyms.items():
        if key in source_lower:
            for syn in syns:
                if syn in field_name.lower() or syn in friendly_name.lower():
                    return 0.7
    source_tokens = set(re.findall(r"\w+", source_lower))
    target_tokens = set(re.findall(r"\w+", field_name.lower() + " " + friendly_name.lower()))
    overlap = len(source_tokens & target_tokens)
    union = len(source_tokens | target_tokens)
    if union > 0:
        return overlap / union
    return 0.0
