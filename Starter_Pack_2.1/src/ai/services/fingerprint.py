# src/ai/services/fingerprint.py
import hashlib

def compute_file_hash(file_bytes: bytes) -> str:
    """Return SHA-256 hex digest of file content."""
    return hashlib.sha256(file_bytes).hexdigest()
