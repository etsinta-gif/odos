# src/ai/services/template_matcher.py
import json
from sqlalchemy.orm import Session
from src.ai.models import AI_Metadata

def find_matching_template(db: Session, company_id: int, current_headers: list) -> dict:
    """Return the best matching template (metadata record) with confidence."""
    templates = db.query(AI_Metadata).filter(
        AI_Metadata.company_id == company_id,
        AI_Metadata.source_system != "UNKNOWN",
        AI_Metadata.header_columns.isnot(None)
    ).all()
    
    best_match = None
    best_score = 0.0
    for tmpl in templates:
        stored_headers = json.loads(tmpl.header_columns)
        # Compute Jaccard similarity
        intersection = len(set(current_headers) & set(stored_headers))
        union = len(set(current_headers) | set(stored_headers))
        score = intersection / union if union > 0 else 0
        if score > best_score:
            best_score = score
            best_match = tmpl
    return {"template": best_match, "confidence": best_score}
