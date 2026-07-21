# src/ai/services/pattern_detector.py
import re
from typing import List, Dict, Any

def detect_patterns(column_values: List[str]) -> Dict[str, Any]:
    """Detect patterns like date, PAN, amount, percentage."""
    patterns = {}
    # Date pattern (YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY, etc.)
    date_pattern = r'\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4}|\d{2}/\d{2}/\d{4}'
    if any(re.search(date_pattern, str(v)) for v in column_values if v):
        patterns['is_date'] = True
    # PAN pattern (5 letters, 4 digits, 1 letter)
    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
    if any(re.search(pan_pattern, str(v)) for v in column_values if v):
        patterns['is_pan'] = True
    # Amount pattern (numbers with commas, optional decimals)
    amount_pattern = r'^\d{1,3}(,\d{3})*(\.\d{1,2})?$'
    if any(re.match(amount_pattern, str(v)) for v in column_values if v):
        patterns['is_amount'] = True
    # Percentage pattern (number followed by %)
    percent_pattern = r'\d+(\.\d+)?%'
    if any(re.search(percent_pattern, str(v)) for v in column_values if v):
        patterns['is_percentage'] = True
    return patterns
