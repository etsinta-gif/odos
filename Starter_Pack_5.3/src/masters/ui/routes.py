from pathlib import Path
from typing import Optional

from fastapi import APIRouter, File, Form, Request, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..api.document import DOCUMENT_STORE, delete_document, download_document, upload_document, DocumentIn

router = APIRouter(prefix="/masters/documents", tags=["masters"])

TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


def get_active_documents():
    return [doc for doc in DOCUMENT_STORE.values() if doc["is_active"]]


@router.get("/", response_class=HTMLResponse)
async def document_index(request: Request):
    documents = get_active_documents()
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
):
    document_payload = DocumentIn(
        case_id=case_id,
        customer_id=customer_id,
        lender_id=lender_id,
        document_type=document_type,
        uploaded_by=uploaded_by,
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
