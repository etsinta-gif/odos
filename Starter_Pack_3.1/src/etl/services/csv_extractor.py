# src/etl/services/csv_extractor.py
import csv
from typing import List, Dict, Any

def extract_csv(file_path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
    """Extract data from CSV file."""
    rows = []
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            rows.append(row)
    return rows
