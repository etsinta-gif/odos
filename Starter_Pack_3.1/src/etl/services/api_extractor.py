# src/etl/services/api_extractor.py
import requests
from typing import List, Dict, Any

def extract_api(url: str, headers: dict = None, params: dict = None) -> List[Dict[str, Any]]:
    """Extract data from REST API (placeholder)."""
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data
