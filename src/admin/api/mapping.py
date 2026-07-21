from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.admin.services.file_analyzer import analyze_excel_bytes
from src.admin.services.mapper import generate_mapping_proposal
from src.admin.services.template_store import (
    create_template,
    delete_template,
    get_template,
    list_templates,
    list_templates_scoped,
    update_template,
)
from src.core.database import get_db
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(prefix="/api/admin/mapping", tags=["Admin"])


class ColumnMapping(BaseModel):
    source_column: str
    target_table: str
    target_field: str
    confidence_score: int = 0
    is_verified: bool = False
    is_natural_key: bool = False
    transformation_rule: Optional[str] = None
    notes: Optional[str] = None


class TemplateCreate(BaseModel):
    template_name: str
    file_pattern: Optional[str] = None
    fingerprint: Optional[str] = None
    sheet_name: str = "Sheet1"
    header_row: int = 1
    mappings: list[ColumnMapping]
    conflict_resolution: str = "SKIP"
    version: int = 1
    status: str = "Draft"
    shared: bool = False
    company_id: Optional[int] = None


class TemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    file_pattern: Optional[str] = None
    fingerprint: Optional[str] = None
    mappings: Optional[list[ColumnMapping]] = None
    conflict_resolution: Optional[str] = None
    status: Optional[str] = None


def _ensure_template_access(template, current_user: SEC_User):
    if current_user.has_role("ADMIN"):
        return
    if not template or template.company_id != current_user.company_id:
        raise HTTPException(status_code=404, detail="Template not found")


@router.post("/templates/draft")
def save_template_draft(
    template_data: TemplateCreate,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    payload = template_data.model_dump()
    payload["company_id"] = current_user.company_id
    payload["shared"] = False
    payload["status"] = "Draft"
    template = create_template(db, payload)
    return template


@router.post("/templates/{template_id}/submit")
def submit_template_for_approval(
    template_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    template = get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    _ensure_template_access(template, current_user)
    updated = update_template(db, template_id, {"status": "Approved"})
    if not updated:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated


@router.post("/templates/{template_id}/activate")
def activate_template(
    template_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.has_role("ADMIN"):
        raise HTTPException(status_code=403, detail="Only system admins can activate templates")
    updated = update_template(db, template_id, {"status": "Active"})
    if not updated:
        raise HTTPException(status_code=404, detail="Template not found")
    return updated


@router.post("/analyze")
async def analyze_excel_file(
    file: UploadFile = File(...),
    sheet_name: Optional[str] = Form(None),
    header_row: int = Form(1),
):
    try:
        file_bytes = await file.read()
        analysis = analyze_excel_bytes(file_bytes, sheet_name=sheet_name, header_row=header_row)
        proposal = generate_mapping_proposal(analysis)
        proposal["file_name"] = file.filename
        proposal["analyzed_at"] = datetime.utcnow().isoformat()
        return proposal
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/confirm")
def confirm_mapping(
    template_data: TemplateCreate,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.has_role("ADMIN"):
        raise HTTPException(status_code=403, detail="Only system admins can create templates")

    payload = template_data.model_dump()
    payload["company_id"] = None if payload.get("shared") else (payload.get("company_id") or current_user.company_id)
    payload["status"] = payload.get("status") or "Draft"
    template = create_template(db, payload)
    return template


@router.get("/templates")
def list_templates_endpoint(current_user: SEC_User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.has_role("ADMIN"):
        return list_templates(db)
    return list_templates_scoped(db, current_user.company_id)


@router.get("/templates/{template_id}")
def get_template_endpoint(
    template_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    template = get_template(db, template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    if not current_user.has_role("ADMIN") and not (template.shared or template.company_id == current_user.company_id):
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.put("/templates/{template_id}")
def update_template_endpoint(
    template_id: int,
    template_data: TemplateUpdate,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.has_role("ADMIN"):
        raise HTTPException(status_code=403, detail="Only system admins can update templates")
    payload = {k: v for k, v in template_data.model_dump().items() if v is not None}
    template = update_template(db, template_id, payload)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template


@router.delete("/templates/{template_id}")
def delete_template_endpoint(
    template_id: int,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.has_role("ADMIN"):
        raise HTTPException(status_code=403, detail="Only system admins can delete templates")
    deleted = delete_template(db, template_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"message": "Template deleted"}
