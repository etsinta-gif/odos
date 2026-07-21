# src/ai/services/source_detector.py
import re
from typing import List

def detect_source(file_name: str, sheet_names: List[str], headers: List[str]) -> str:
    """Return a likely source system name based on keywords."""
    combined = (file_name + " " + " ".join(sheet_names) + " " + " ".join(headers)).lower()
    if re.search(r'hdfc', combined):
        return "HDFC"
    if re.search(r'sbi|state bank', combined):
        return "SBI"
    if re.search(r'axis', combined):
        return "AXIS"
    if re.search(r'icici', combined):
        return "ICICI"
    if re.search(r'kotak', combined):
        return "KOTAK"
    if re.search(r'tata', combined):
        return "TATA"
    if re.search(r'indifi', combined):
        return "INDIFI"
    if re.search(r'piramal', combined):
        return "PIRAMAL"
    return "UNKNOWN"
