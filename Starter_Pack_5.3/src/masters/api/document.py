from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Optional

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/masters/documents", tags=["masters"])

UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "docx", "png", "jpg", "jpeg"}
MAX_UPLOAD_SIZE = 10 * 1024 * 1024

# In a real implementation, these would talk to a database session / ORM models.
DOCUMENT_STORE = {}
FILE_REPOSITORY = {}
NEXT_DOCUMENT_ID = 1
NEXT_FILE_ID = 1


class DocumentIn(BaseModel):
    case_id: Optional[int] = None
    customer_id: Optional[int] = None
    lender_id: Optional[int] = None
    document_type: str
    uploaded_by: str

    @classmethod
    def as_form(cls,
                case_id: Optional[int] = Form(None),
                customer_id: Optional[int] = Form(None),
                lender_id: Optional[int] = Form(None),
                document_type: str = Form(...),
                uploaded_by: str = Form(...)):
        return cls(
            case_id=case_id,
            customer_id=customer_id,
            lender_id=lender_id,
            document_type=document_type,
            uploaded_by=uploaded_by,
        )


class DocumentOut(DocumentIn):
    document_id: int
    filename: str
    content_type: str
    file_size: int
    file_hash: str
    uploaded_at: datetime
    is_active: bool


class FileRepositoryOut(BaseModel):
    file_repository_id: int
    filename: str
    file_hash: str
    file_size: int
    content_type: str
    file_path: str
    created_at: datetime
    is_active: bool


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


async def compute_file_hash(upload_file: UploadFile) -> str:
    hasher = sha256()
    await upload_file.seek(0)
    while chunk := await upload_file.read(1024 * 1024):
        hasher.update(chunk)
    await upload_file.seek(0)
    return hasher.hexdigest()


async def save_upload(upload_file: UploadFile, destination: Path) -> int:
    size = 0
    await upload_file.seek(0)
    async with aiofiles.open(destination, "wb") as out_file:
        while chunk := await upload_file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_UPLOAD_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File exceeds maximum upload size")
            await out_file.write(chunk)
    await upload_file.seek(0)
    return size


@router.post("/upload", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
async def upload_document(document: DocumentIn = Depends(DocumentIn.as_form), file: UploadFile = File(...)):
    extension = get_extension(file.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type")

    file_hash = await compute_file_hash(file)
    global NEXT_FILE_ID, NEXT_DOCUMENT_ID
    file_repository_id = NEXT_FILE_ID
    document_id = NEXT_DOCUMENT_ID
    stored_filename = f"{file_repository_id}_{file.filename}"
    file_path = UPLOAD_DIR / stored_filename
    file_size = await save_upload(file, file_path)

    now = datetime.utcnow()
    FILE_REPOSITORY[file_repository_id] = {
        "file_repository_id": file_repository_id,
        "filename": file.filename,
        "file_hash": file_hash,
        "file_size": file_size,
        "content_type": file.content_type,
        "file_path": str(file_path),
        "created_at": now,
        "is_active": True,
    }
    DOCUMENT_STORE[document_id] = {
        "document_id": document_id,
        "case_id": document.case_id,
        "customer_id": document.customer_id,
        "lender_id": document.lender_id,
        "document_type": document.document_type,
        "uploaded_by": document.uploaded_by,
        "uploaded_at": now,
        "filename": file.filename,
        "content_type": file.content_type,
        "file_size": file_size,
        "file_hash": file_hash,
        "file_repository_id": file_repository_id,
        "is_active": True,
    }
    NEXT_FILE_ID += 1
    NEXT_DOCUMENT_ID += 1

    return {**DOCUMENT_STORE[document_id]}


@router.get("/", response_model=list[DocumentOut])
async def list_documents():
    return [doc for doc in DOCUMENT_STORE.values() if doc["is_active"]]


@router.get("/{document_id}", response_model=DocumentOut)
async def get_document(document_id: int):
    document = DOCUMENT_STORE.get(document_id)
    if not document or not document["is_active"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return document


@router.get("/download/{document_id}")
async def download_document(document_id: int):
    document = DOCUMENT_STORE.get(document_id)
    if not document or not document["is_active"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    file_repo = FILE_REPOSITORY.get(document["file_repository_id"])
    if not file_repo or not file_repo["is_active"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(path=file_repo["file_path"], filename=file_repo["filename"], media_type=file_repo["content_type"])


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: int):
    document = DOCUMENT_STORE.get(document_id)
    if not document or not document["is_active"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    document["is_active"] = False
    file_repo = FILE_REPOSITORY.get(document["file_repository_id"])
    if file_repo:
        file_repo["is_active"] = False
    return None
