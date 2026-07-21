import os
import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.admin.services.file_analyzer import analyze_excel_bytes
from src.admin.services.mapper import generate_mapping_proposal
from src.ai.services.feedback import create_ai_metadata, record_learning_event, record_mapping_feedback, record_mapping_snapshot
from src.core.database import get_db
from src.masters.api import etl as etl_api
from src.masters.models import MST_Connector, MST_DSA, MST_Lender
from src.metadata.services.fixed_templates import FIXED_TEMPLATE_OPTIONS, FIXED_TEMPLATE_NAME_SET
from src.security.auth import get_current_user
from src.security.models import SEC_User
from src.transactions.models import ETL_ImportBatch, TRN_Case, TRN_Commission, TRN_Revenue

router = APIRouter(prefix="/masters", tags=["ETL UI"], dependencies=[Depends(get_current_user)])
templates = Jinja2Templates(directory="src/templates")

UPLOAD_DIR = "uploads/etl"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def _sheet_domain_context(sheet_name: str) -> list[str]:
    normalized = (sheet_name or "").strip().lower()
    context: list[str] = []
    if "lender" in normalized or normalized in {"bl", "pl"} or "mis" in normalized:
        context.append("lender")
    if "product" in normalized or "payout" in normalized or normalized in {"bl", "pl"}:
        context.append("product")
    if "master" in normalized:
        context.append("master")
    return context


def _sheet_business_scope(sheet_name: str) -> str:
    normalized = (sheet_name or "").strip().lower()
    if normalized in {"bl", "pl"} or "mis" in normalized or "payout" in normalized:
        return "PRE_DISBURSEMENT_MIS"
    return "GENERIC"


def _upload_page_context(request: Request, db: Session, company_id: int, extra: dict | None = None) -> dict:
    batches = (
        db.query(ETL_ImportBatch)
        .filter(ETL_ImportBatch.company_id == company_id)
        .order_by(ETL_ImportBatch.import_datetime.desc())
        .all()
    )
    active_dsa = db.query(MST_DSA).filter(MST_DSA.is_active == True).order_by(MST_DSA.dsa_id.asc()).first()
    latest_staged_batch = (
        db.query(ETL_ImportBatch)
        .filter(ETL_ImportBatch.company_id == company_id)
        .filter(ETL_ImportBatch.import_status == "STAGED")
        .order_by(ETL_ImportBatch.import_datetime.desc())
        .first()
    )
    context = {
        "request": request,
        "batches": batches,
        "success": request.query_params.get("success"),
        "error": request.query_params.get("error"),
        "active_dsa": active_dsa,
        "fixed_template_options": FIXED_TEMPLATE_OPTIONS,
        "latest_staged_batch": latest_staged_batch,
    }
    if extra:
        context.update(extra)
    return context


@router.get("/etl/upload", response_class=HTMLResponse)
def upload_form(
    request: Request,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse("masters/etl_upload.html", _upload_page_context(request, db, current_user.company_id))


@router.post("/etl/upload")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    template_name: str = Form(...),
    intent: str = Form("upload"),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    selected_template_name = str(template_name or "").strip()
    if selected_template_name not in FIXED_TEMPLATE_NAME_SET:
        return templates.TemplateResponse(
            "masters/etl_upload.html",
                _upload_page_context(request, db, current_user.company_id, {"error": "Invalid template selected. Only approved MIS templates are allowed."}),
        )

    try:
        file_bytes = await file.read()
        if intent == "analyze":
            template_validation = etl_api.validate_upload_template_bytes(
                file_bytes,
                selected_template_name,
                db,
                current_user.company_id,
            )
            if not template_validation.get("ok"):
                return templates.TemplateResponse(
                    "masters/etl_upload.html",
                    _upload_page_context(
                        request,
                        db,
                        current_user.company_id,
                        {
                            "error": template_validation.get("message"),
                            "template_missing_columns": template_validation.get("missing_columns") or [],
                            "selected_template_name": selected_template_name,
                        },
                    ),
                )

            template = template_validation["template"]
            analysis = analyze_excel_bytes(file_bytes, sheet_name=template.sheet_name, header_row=template.header_row)
            proposal = generate_mapping_proposal(analysis)
            sheets = proposal.get("sheets", []) or []
            selected_sheet_index = 0 if sheets else None
            selected_sheet = sheets[selected_sheet_index]["sheet_name"] if sheets else None
            return templates.TemplateResponse(
                "masters/etl_upload.html",
                _upload_page_context(request, db, current_user.company_id, {
                    "analysis_proposal": proposal,
                    "analysis_proposal_json": json.dumps(proposal, default=str),
                    "analysis_file_name": file.filename,
                    "analysis_template_name": selected_template_name,
                    "analysis_selected_sheet": selected_sheet,
                    "analysis_selected_sheet_index": selected_sheet_index,
                    "selected_template_name": selected_template_name,
                }),
            )

        result = etl_api.upload_to_staging_bytes(
            file_bytes,
            file.filename or "",
            selected_template_name,
            current_user.company_id,
            db,
            selected_template_name=selected_template_name,
            strict_template=True,
        )
    except Exception as exc:
        return RedirectResponse(url=f"/masters/etl/upload?error={str(exc)}", status_code=303)

    if isinstance(result, dict) and result.get("status_code") in {400, 422}:
        return templates.TemplateResponse(
            "masters/etl_upload.html",
            _upload_page_context(
                request,
                db,
                current_user.company_id,
                {
                    "error": result.get("message"),
                    "template_missing_columns": result.get("missing_columns") or [],
                    "selected_template_name": selected_template_name,
                },
            ),
        )

    if isinstance(result, dict) and result.get("status_code") == 202:
        proposal = result.get("proposal") or {}
        sheets = proposal.get("sheets", []) or []
        selected_sheet_index = 0 if sheets else None
        selected_sheet = sheets[selected_sheet_index]["sheet_name"] if sheets else None
        return templates.TemplateResponse(
            "masters/etl_upload.html",
            _upload_page_context(request, db, current_user.company_id, {
                "analysis_proposal": proposal,
                "analysis_proposal_json": json.dumps(proposal, default=str),
                "analysis_file_name": file.filename,
                "analysis_template_name": selected_template_name,
                "analysis_selected_sheet": selected_sheet,
                "analysis_selected_sheet_index": selected_sheet_index,
                "error": result.get("message"),
            }),
        )

    if isinstance(result, dict) and result.get("status_code") == 409:
        return templates.TemplateResponse(
            "masters/etl_upload.html",
            _upload_page_context(request, db, current_user.company_id, {"error": result.get("message")} ),
        )

    return RedirectResponse(
        url=f"/masters/etl/upload?success=Batch {result['batch_guid']} staged with {result['staged_rows']} rows",
        status_code=303,
    )


@router.post("/etl/template/approve")
def approve_template_from_analysis(
    proposal_json: str = Form(...),
    sheet_name: str = Form(...),
    template_name: str = Form(...),
    file_pattern: str | None = Form(None),
    conflict_resolution: str = Form("SKIP"),
    db: Session = Depends(get_db),
):
    raise HTTPException(status_code=403, detail="Template approval/creation is disabled. Only pre-approved MIS templates are allowed.")

    proposal = json.loads(proposal_json)
    sheets = proposal.get("sheets") or []
    selected_sheet = next((sheet for sheet in sheets if sheet.get("sheet_name") == sheet_name), None)
    if not selected_sheet:
        raise HTTPException(status_code=400, detail="Selected sheet not found in analysis proposal")

    mappings = []
    for column in selected_sheet.get("columns", []):
        if column.get("ignore"):
            continue
        target_table = column.get("suggested_target_table")
        target_field = column.get("suggested_target_field")
        if not target_table or not target_field:
            continue
        source_column = column.get("source_column")
        source_norm = str(source_column or "").strip().lower()
        transformation_payload = {}
        for key in (
            "lookup",
            "transformation",
            "condition",
            "repeat_for",
            "tier_min",
            "tier_max",
            "target_fields",
            "confidence_level",
            "formula_detected",
            "formula_count",
            "formula_error_count",
            "formula_samples",
            "evaluated_formula_samples",
            "formula_status",
        ):
            value = column.get(key)
            if value not in (None, "", [], {}):
                transformation_payload[key] = value
        mappings.append(
            {
                "source_column": source_column,
                "target_table": target_table,
                "target_field": target_field,
                "confidence_score": int(column.get("confidence_score") or 0),
                "confidence_level": column.get("confidence_level") or None,
                "is_verified": True,
                "is_natural_key": source_norm in {"pan", "lender_code", "connector_code", "registration_id", "case_number", "dsa_code"},
                "formula_detected": bool(column.get("formula_detected")),
                "formula_status": column.get("formula_status") or None,
                "transformation_rule": json.dumps(transformation_payload, default=str) if transformation_payload else None,
                "notes": column.get("notes"),
            }
        )

    if not mappings:
        raise HTTPException(status_code=400, detail="No mapped columns available to approve")

    payload = {
        "template_name": template_name,
        "file_pattern": file_pattern or (proposal.get("file_name") or template_name),
        "fingerprint": selected_sheet.get("fingerprint"),
        "sheet_name": selected_sheet.get("sheet_name"),
        "header_row": selected_sheet.get("header_row") or 1,
        "mappings": mappings,
        "conflict_resolution": str(conflict_resolution or "SKIP").upper(),
        "version": 1,
        "status": "Active",
    }
    template = create_template(db, payload)
    domain_context = _sheet_domain_context(template.sheet_name)
    business_scope = _sheet_business_scope(template.sheet_name)

    metadata = create_ai_metadata(
        db,
        file_name=template.template_name,
        file_hash=template.fingerprint or template.template_name,
        source_system="FCPL_Excel",
        sheet_name=template.sheet_name,
        header_columns=[mapping.get("source_column") for mapping in mappings],
        data_types={mapping.get("source_column"): mapping.get("target_field") for mapping in mappings},
        row_count=None,
        import_batch_guid=None,
        confidence=None,
        company_id=1,
    )
    metadata_id = metadata.metadata_id
    learning_payload = {
        "template_name": template.template_name,
        "file_pattern": payload.get("file_pattern"),
        "sheet_name": template.sheet_name,
        "domain_context": domain_context,
        "business_scope": business_scope,
        "mappings": mappings,
    }
    for mapping in mappings:
        try:
            mapping_snapshot = record_mapping_snapshot(
                db,
                metadata_id=metadata_id,
                source_column=mapping.get("source_column"),
                target_table=mapping.get("target_table"),
                target_field=mapping.get("target_field"),
                confidence=float(mapping.get("confidence_score") or 0),
                is_verified=bool(mapping.get("is_verified", True)),
                notes=mapping.get("notes"),
            )
            record_mapping_feedback(
                db,
                metadata_id=metadata_id,
                template_id=template.template_id,
                batch_guid=None,
                sheet_name=template.sheet_name,
                source_column=mapping.get("source_column"),
                target_table=mapping.get("target_table"),
                target_field=mapping.get("target_field"),
                confidence_score=int(mapping.get("confidence_score") or 0),
                confidence_level=mapping.get("confidence_level"),
                formula_detected=bool(mapping.get("formula_detected")),
                formula_status=str(mapping.get("formula_status") or None),
                user_decision="APPROVED",
                discrepancy_reason=mapping.get("notes"),
                payload={"template_id": template.template_id, "mapping_snapshot_id": mapping_snapshot.mapping_id, "metadata_id": metadata_id, "domain_context": domain_context, "business_scope": business_scope},
            )
        except Exception:
            # Feedback capture must not block template approval.
            pass

    try:
        record_learning_event(
            db,
            metadata_id=metadata_id,
            mapping_id=None,
            event_type="TEMPLATE_APPROVED",
            payload=learning_payload,
            model_name="mapping-analyzer",
            model_version="1.0",
            confidence_before=None,
            confidence_after=None,
        )
    except Exception:
        pass

    db.commit()
    return RedirectResponse(
        url=f"/masters/etl/upload?success=Template {template.template_name} approved and activated for {template.sheet_name}",
        status_code=303,
    )


@router.get("/reports/pilot", response_class=HTMLResponse)
def pilot_report(
    request: Request,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connector_count = db.query(MST_Connector).filter(MST_Connector.company_id == current_user.company_id).count()
    lender_count = db.query(MST_Lender).filter(MST_Lender.company_id == current_user.company_id).count()
    case_count = db.query(TRN_Case).filter(TRN_Case.company_id == current_user.company_id).count()
    revenue_count = db.query(TRN_Revenue).filter(TRN_Revenue.company_id == current_user.company_id).count()
    commission_count = db.query(TRN_Commission).filter(TRN_Commission.company_id == current_user.company_id).count()

    return templates.TemplateResponse(
        "masters/pilot_report.html",
        {
            "request": request,
            "connector_count": connector_count,
            "lender_count": lender_count,
            "case_count": case_count,
            "revenue_count": revenue_count,
            "commission_count": commission_count,
        },
    )