"""ETL API stub for IMP-1.5."""

from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
def upload_file():
    return {"status": "ok", "message": "upload endpoint stub"}

@router.get("/batches")
def list_batches():
    return {"batches": []}

@router.get("/staging")
def list_staging():
    return {"staging": []}

@router.get("/errors")
def list_errors():
    return {"errors": []}
