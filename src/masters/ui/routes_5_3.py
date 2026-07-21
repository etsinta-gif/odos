from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..api.document import DOCUMENT_STORE, delete_document, download_document, upload_document, DocumentIn
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(prefix="/masters/documents", tags=["masters"], dependencies=[Depends(get_current_user)])

TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


def get_active_documents(current_username: str):
    return [doc for doc in DOCUMENT_STORE.values() if doc["is_active"] and doc.get("uploaded_by") == current_username]


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def document_index(request: Request, current_user: SEC_User = Depends(get_current_user)):
    documents = get_active_documents(current_user.username)
    return TEMPLATES.TemplateResponse("masters/documents.html", {"request": request, "documents": documents})


@router.post("/upload")
async def document_upload(
    request: Request,
    case_id: Optional[int] = Form(None),
    customer_id: Optional[int] = Form(None),
    lender_id: Optional[int] = Form(None),
    document_type: str = Form(...),
    uploaded_by: str = Form(...),
    file: UploadFile = File(...),
    current_user: SEC_User = Depends(get_current_user),
):
    document_payload = DocumentIn(
        case_id=case_id,
        customer_id=customer_id,
        lender_id=lender_id,
        document_type=document_type,
        uploaded_by=current_user.username or uploaded_by,
    )
    await upload_document(document=document_payload, file=file)
    return RedirectResponse(url="/masters/documents", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/download/{document_id}")
async def document_download(document_id: int):
    return await download_document(document_id)


@router.post("/delete/{document_id}")
async def document_delete(document_id: int):
    await delete_document(document_id)
    return RedirectResponse(url="/masters/documents", status_code=status.HTTP_303_SEE_OTHER)
