# src/etl/services/excel_extractor.py
import pandas as pd
from typing import List, Dict, Any

def extract_excel(file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
    """Extract data from Excel file and return list of rows as dicts."""
    if sheet_name is None:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    records = df.to_dict(orient='records')
    return records
