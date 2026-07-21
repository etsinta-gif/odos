from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOAD_DIR = BASE_DIR / "uploads" / "documents"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

sample_file_path = BASE_DIR / "sample.pdf"
if not sample_file_path.exists():
    with open(sample_file_path, "wb") as f:
        f.write(b"%PDF-1.4\n% test pdf sample\n")

print("Created sample document at:", sample_file_path)
print("Use the API endpoint /api/masters/documents/upload to upload this sample file.")
