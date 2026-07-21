# src/ai/services/mapping_validator.py
def validate_mapping_suggestion(suggestion: dict, min_confidence: float = 0.5) -> bool:
    """Return True if suggestion confidence is above threshold."""
    return suggestion.get("confidence", 0.0) >= min_confidence
