# src/etl/validators/file_validator.py
import os

def validate_file(file_path: str, allowed_extensions: list = ['.xlsx', '.xls', '.csv']):
    """Check file extension and existence."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"Unsupported file type: {ext}. Allowed: {allowed_extensions}")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return True
