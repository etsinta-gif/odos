import hashlib
import json
import math
import uuid
from datetime import datetime
from io import BytesIO
from typing import Any, Optional
import re
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.admin.services.file_analyzer import analyze_excel_bytes
from src.admin.services.mapper import generate_mapping_proposal
from src.core.database import get_db
from src.etl.services.promoter import promote_batch, supports_multi_target
from src.masters.models import MST_Connector, MST_DSA, MST_Lender
from src.metadata.models import META_FieldMapping, META_ImportTemplate
from src.metadata.services.field_mapper import get_template_by_fingerprint, get_template_by_name, get_template_by_pattern
from src.metadata.services.fixed_templates import FIXED_TEMPLATE_NAME_SET, FIXED_TEMPLATE_PRIMARY_TABLE
from src.rules.api.rules import RuleExecutionRequest, execute_validation_rules
from src.security.auth import get_current_user
from src.security.models import SEC_User
from src.transactions.models import (
    ETL_DataLineage,
    ETL_ErrorLog,
    ETL_ImportBatch,
    RUL_CommissionSlab,
    ETL_StagingRawData,
    TRN_Case,
    TRN_Commission,
    TRN_Revenue,
)

router = APIRouter(prefix="/api/v1/etl", tags=["ETL"])


def _to_bool_form(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def compute_file_hash(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def _json_safe(value: Any) -> Any:
    # Convert pandas/numpy datetime-like values (and other non-JSON types) to strings.
    return json.loads(json.dumps(value, default=str))


def _analyze_csv_bytes(file_bytes: bytes, file_name: str) -> dict[str, Any]:
    df = pd.read_csv(BytesIO(file_bytes))
    columns: list[dict[str, Any]] = []
    for col in df.columns:
        series = df[col]
        non_null = series.dropna()
        sample_values = non_null.head(5).tolist()
        columns.append(
            {
                "source_column": str(col),
                "inferred_type": "amount" if pd.api.types.is_numeric_dtype(series) else "text",
                "sample_values": sample_values,
                "null_count": int(series.isna().sum()),
                "unique_count": int(non_null.nunique()) if len(non_null) else 0,
                "pattern": None,
                "formula_detected": False,
                "formula_count": 0,
                "formula_error_count": 0,
                "formula_samples": [],
                "evaluated_formula_samples": [],
                "formula_status": "NONE",
                "suggested_target_table": None,
                "suggested_target_field": None,
                "confidence_score": 0,
                "ignore": False,
                "notes": None,
            }
        )

    sheet_fingerprint_data = f"CSV|{file_name}|{'|'.join([c['source_column'] for c in columns])}"
    sheet_fingerprint = hashlib.sha256(sheet_fingerprint_data.encode()).hexdigest()
    return {
        "workbook_fingerprint": hashlib.sha256(f"WORKBOOK|{sheet_fingerprint}".encode()).hexdigest(),
        "sheet_count": 1,
        "sheets": [
            {
                "fingerprint": sheet_fingerprint,
                "sheet_name": "CSV",
                "header_row": 1,
                "row_count": len(df),
                "columns": columns,
            }
        ],
    }


def create_batch(db: Session, company_id: int, file_name: str, entity_type: str) -> str:
    batch_guid = str(uuid.uuid4())
    batch = ETL_ImportBatch(
        batch_guid=batch_guid,
        company_id=company_id,
        source_system="FCPL",
        file_name=file_name,
        import_status="STAGED",
        is_atomic_transaction=False,
        is_complete=False,
        import_datetime=datetime.utcnow(),
        total_rows=0,
        successful_rows=0,
        failed_rows=0,
    )
    db.add(batch)
    db.commit()
    return batch_guid


def _find_duplicate_batch(db: Session, file_hash: str, company_id: int) -> ETL_ImportBatch | None:
    return (
        db.query(ETL_ImportBatch)
        .filter(ETL_ImportBatch.file_hash == file_hash)
        .filter(ETL_ImportBatch.company_id == company_id)
        .filter(ETL_ImportBatch.import_status != "DELETED")
        .order_by(ETL_ImportBatch.import_datetime.desc())
        .first()
    )


def _loads_row(raw: str) -> dict[str, Any]:
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _pick(row: dict[str, Any], *keys: str, default: Any = None) -> Any:
    lowered = {str(k).strip().lower(): v for k, v in row.items()}
    for key in keys:
        val = lowered.get(key.strip().lower())
        if val not in (None, ""):
            return val
    return default


def _map_table(entity_type: str) -> str:
    mapping = {
        "connector": "MST_Connector",
        "lender": "MST_Lender",
        "case": "TRN_Case",
        "slab": "RUL_CommissionSlab",
        "rul_commission_slab": "RUL_CommissionSlab",
        "mst_connector": "MST_Connector",
        "mst_lender": "MST_Lender",
        "trn_case": "TRN_Case",
    }
    return mapping.get(entity_type.strip().lower(), entity_type)


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def _norm_col(value: str) -> str:
    norm = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
    norm = re.sub(r"_+", "_", norm).strip("_")
    return norm


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _to_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    if isinstance(value, (int, float)):
        num = float(value)
        return num if math.isfinite(num) else default

    text = str(value).strip()
    text = text.replace("%", "").replace(",", "")
    text = text.replace("₹", "").replace("INR", "")
    try:
        num = float(text)
        return num if math.isfinite(num) else default
    except Exception:
        return default


def _normalize_by_mapping(row: dict[str, Any], mappings: list[dict[str, Any]], target_table: str) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    lowered = {_norm_col(str(k)): v for k, v in row.items()}

    for mapping in mappings:
        if mapping.get("target_table") != target_table:
            continue
        source = _norm_col(str(mapping.get("source_column", "")))
        target = str(mapping.get("target_field", "")).strip()
        if not source or not target:
            continue
        if source in lowered:
            normalized[target] = _sanitize_value(lowered[source])

    # Fallback for previous behavior if mapping is incomplete.
    if target_table == "MST_Connector":
        normalized.setdefault("connector_code", _sanitize_value(_pick(row, "connector_code", "connector code")))
        normalized.setdefault("full_name", _sanitize_value(_pick(row, "full_name", "connector_name", "connector name")))
        normalized.setdefault("pan", _sanitize_value(_pick(row, "pan")))
        normalized.setdefault("gstin", _sanitize_value(_pick(row, "gstin")))
        normalized.setdefault("bank_name", _sanitize_value(_pick(row, "bank_name", "bank name")))
        normalized.setdefault("account_number", _sanitize_value(_pick(row, "account_number", "account number")))
        normalized.setdefault("ifsc", _sanitize_value(_pick(row, "ifsc")))
    elif target_table == "MST_Lender":
        normalized.setdefault("lender_name", _sanitize_value(_pick(row, "lender_name", "lender name")))
        normalized.setdefault("pan", _sanitize_value(_pick(row, "pan")))
        normalized.setdefault("gstin", _sanitize_value(_pick(row, "gstin")))
        normalized.setdefault("lender_code", _sanitize_value(_pick(row, "lender_code", "lender code")))
        normalized.setdefault("is_nbfc", _to_bool(_pick(row, "is_nbfc", "is nbfc", default=False)))
    elif target_table == "MST_Product":
        normalized.setdefault("product_name", _sanitize_value(_pick(row, "product_name", "product name", "lending_product")))
        normalized.setdefault("product_code", _sanitize_value(_pick(row, "product_code", "product code")))
        normalized.setdefault("min_loan_amount", _to_float(_pick(row, "min_loan_amount", "min loan amount")))
        normalized.setdefault("max_loan_amount", _to_float(_pick(row, "max_loan_amount", "max loan amount")))
        normalized.setdefault("interest_rate", _to_float(_pick(row, "interest_rate", "interest rate")))
        normalized.setdefault("is_active", _to_bool(_pick(row, "active", "is_active", default=True)))
    elif target_table == "TRN_Case":
        normalized.setdefault("case_number", _sanitize_value(_pick(row, "case_number", "case number")))
        normalized.setdefault("customer_id", _sanitize_value(_pick(row, "customer_id", "customer id")))
        normalized.setdefault("lender_id", _sanitize_value(_pick(row, "lender_id", "lender id")))
        normalized.setdefault("product_id", _sanitize_value(_pick(row, "product_id", "product id")))
        normalized.setdefault("sanction_amount", _sanitize_value(_pick(row, "sanction_amount", "sanction amount")))
        normalized.setdefault("disbursement_amount", _sanitize_value(_pick(row, "disbursement_amount", "disbursement amount")))
        normalized.setdefault("status", _sanitize_value(_pick(row, "status")))
        normalized.setdefault("connector_id", _sanitize_value(_pick(row, "connector_id", "connector id")))

    return {k: v for k, v in normalized.items() if v not in (None, "")}


def _build_slab_rows(row: dict[str, Any], mappings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    slab_rows: list[dict[str, Any]] = []
    source_lookup = {_norm_col(str(k)): v for k, v in row.items()}

    for mapping in mappings:
        if mapping.get("target_table") != "RUL_CommissionSlab":
            continue
        source_column = str(mapping.get("source_column", "")).strip()
        if not source_column:
            continue

        source_key = _norm_col(source_column)
        if source_key not in source_lookup:
            continue

        raw_rate = source_lookup[source_key]
        rate = _to_float(raw_rate, default=float("nan"))
        if not math.isfinite(rate):
            continue
        if rate == 0.0 and str(raw_rate).strip() not in {"0", "0.0"}:
            continue

        slab_rows.append({"slab_label": source_column, "rate": rate})

    return slab_rows


def _validate_upload_against_template(file_bytes: bytes, template: META_ImportTemplate) -> dict[str, Any]:
    try:
        analysis = analyze_excel_bytes(file_bytes, sheet_name=template.sheet_name, header_row=template.header_row)
    except Exception as exc:
        return {
            "ok": False,
            "message": f"Uploaded file does not match template sheet/header requirements: {exc}",
            "missing_columns": [],
            "workbook_fingerprint": None,
        }

    sheets = analysis.get("sheets") or []
    if not sheets:
        return {
            "ok": False,
            "message": "No readable sheets found for selected template.",
            "missing_columns": [],
            "workbook_fingerprint": analysis.get("workbook_fingerprint"),
        }

    detected_columns = {_norm_col(str(col.get("source_column") or "")) for col in (sheets[0].get("columns") or [])}
    try:
        mapping_definition = json.loads(template.mapping_definition or "{}")
    except Exception:
        mapping_definition = {}

    required_columns: list[str] = []
    for mapping in mapping_definition.get("mappings", []) or []:
        source_column = str(mapping.get("source_column") or "").strip()
        if source_column:
            required_columns.append(source_column)

    missing_columns = sorted(
        {
            source_column
            for source_column in required_columns
            if _norm_col(source_column) not in detected_columns
        }
    )

    if missing_columns:
        return {
            "ok": False,
            "message": "Uploaded file does not match selected template columns.",
            "missing_columns": missing_columns,
            "workbook_fingerprint": analysis.get("workbook_fingerprint"),
        }

    return {
        "ok": True,
        "message": "Template match validated.",
        "missing_columns": [],
        "workbook_fingerprint": analysis.get("workbook_fingerprint"),
    }


def validate_upload_template_bytes(
    file_bytes: bytes,
    selected_template_name: str,
    db: Session,
    company_id: int,
) -> dict[str, Any]:
    if selected_template_name not in FIXED_TEMPLATE_NAME_SET:
        return {
            "ok": False,
            "status_code": 400,
            "message": "Invalid template selection. Choose one of the approved MIS templates.",
            "missing_columns": [],
            "template": None,
        }

    template = get_template_by_name(db, selected_template_name, company_id=company_id)
    if not template:
        return {
            "ok": False,
            "status_code": 422,
            "message": f"Selected template '{selected_template_name}' is not active in the system.",
            "missing_columns": [],
            "template": None,
        }

    validation = _validate_upload_against_template(file_bytes, template)
    validation["template"] = template
    validation["status_code"] = 200 if validation.get("ok") else 422
    return validation


def upload_to_staging_bytes(
    file_bytes: bytes,
    file_name: str,
    entity_type: str,
    company_id: int,
    db: Session,
    selected_template_name: str | None = None,
    strict_template: bool = False,
) -> dict[str, Any]:
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    table_name = _map_table(entity_type)
    file_hash = compute_file_hash(file_bytes)

    duplicate_batch = _find_duplicate_batch(db, file_hash, company_id)
    if duplicate_batch:
        return {
            "status_code": 409,
            "message": f"This file was already uploaded in batch {duplicate_batch.batch_guid}. Open that batch or upload a different file.",
            "batch_guid": duplicate_batch.batch_guid,
            "file_name": duplicate_batch.file_name,
            "file_hash": file_hash,
        }

    template = None
    workbook_fingerprint = None
    if strict_template:
        if not selected_template_name or selected_template_name not in FIXED_TEMPLATE_NAME_SET:
            return {
                "status_code": 400,
                "message": "Invalid template selection. Choose one of the approved MIS templates.",
            }
        template = get_template_by_name(db, selected_template_name, company_id=company_id)
        if not template:
            return {
                "status_code": 422,
                "message": f"Selected template '{selected_template_name}' is not active in the system.",
            }

        validation = _validate_upload_against_template(file_bytes, template)
        workbook_fingerprint = validation.get("workbook_fingerprint")
        if not validation.get("ok"):
            return {
                "status_code": 422,
                "message": validation.get("message"),
                "missing_columns": validation.get("missing_columns") or [],
                "selected_template": selected_template_name,
            }

        table_name = FIXED_TEMPLATE_PRIMARY_TABLE.get(selected_template_name, table_name)
    else:
        file_suffix = Path(file_name or "").suffix.lower()
        try:
            if file_suffix == ".csv":
                analysis = _analyze_csv_bytes(file_bytes, file_name)
            else:
                analysis = analyze_excel_bytes(file_bytes, sheet_name=None, header_row=1)
        except Exception as exc:
            return {
                "status_code": 422,
                "message": f"Unable to analyze uploaded file: {exc}",
                "file_name": file_name,
                "entity_type": entity_type,
            }
        workbook_fingerprint = analysis["workbook_fingerprint"]

        template = get_template_by_fingerprint(db, workbook_fingerprint, company_id=company_id)
        if not template:
            template = get_template_by_pattern(db, file_name or "", company_id=company_id)

        if not template:
            proposal = generate_mapping_proposal(analysis)
            return {
                "status_code": 202,
                "message": "Template not found. Please analyze and confirm mapping first.",
                "file_name": file_name,
                "file_hash": file_hash,
                "entity_type": entity_type,
                "workbook_fingerprint": workbook_fingerprint,
                "mapping_required": True,
                "proposal": _json_safe(proposal),
            }

    try:
        df = pd.read_excel(BytesIO(file_bytes), sheet_name=template.sheet_name, header=template.header_row - 1)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error reading mapped sheet: {exc}") from exc

    try:
        mapping_definition = json.loads(template.mapping_definition or "{}")
    except Exception:
        mapping_definition = {}

    mappings = mapping_definition.get("mappings", [])
    batch_guid = create_batch(db, company_id=company_id, file_name=file_name, entity_type=table_name)
    batch = db.query(ETL_ImportBatch).filter(ETL_ImportBatch.batch_guid == batch_guid).first()
    batch.file_hash = file_hash
    batch.template_id = template.template_id

    dedupe_keys: set[str] = set()
    staged_rows = 0
    duplicate_rows = 0
    mapped_tables = {str(m.get("target_table", "")).strip() for m in mappings if m.get("target_table")}
    include_slab_rows = "RUL_CommissionSlab" in mapped_tables
    multi_target_mode = supports_multi_target(mappings)

    for idx, row in df.iterrows():
        source_row = row.to_dict()

        if multi_target_mode:
            raw_json = json.dumps(source_row, default=str, sort_keys=True)
            dedupe_key = f"RAW|{raw_json}"
            if dedupe_key in dedupe_keys:
                duplicate_rows += 1
                continue
            dedupe_keys.add(dedupe_key)
            db.add(
                ETL_StagingRawData(
                    batch_guid=batch_guid,
                    company_id=company_id,
                    table_name=table_name,
                    column_name="row_data",
                    source_row_number=idx + 2,
                    source_column_name="",
                    source_value=raw_json,
                    target_field="",
                    stored_value=raw_json,
                    validation_status="PENDING",
                    import_datetime=datetime.utcnow(),
                )
            )
            staged_rows += 1
            continue

        normalized_row = _normalize_by_mapping(source_row, mappings, table_name)
        if normalized_row:
            row_json = json.dumps(normalized_row, default=str, sort_keys=True)
            dedupe_key = f"{table_name}|{row_json}"
            if dedupe_key in dedupe_keys:
                duplicate_rows += 1
            else:
                dedupe_keys.add(dedupe_key)
                db.add(
                    ETL_StagingRawData(
                        batch_guid=batch_guid,
                        company_id=company_id,
                        table_name=table_name,
                        column_name="row_data",
                        source_row_number=idx + 2,
                        source_column_name="",
                        source_value=row_json,
                        target_field="",
                        stored_value=row_json,
                        validation_status="PENDING",
                        import_datetime=datetime.utcnow(),
                    )
                )
                staged_rows += 1

        if include_slab_rows:
            slab_rows = _build_slab_rows(source_row, mappings)
            for slab_row in slab_rows:
                slab_json = json.dumps(slab_row, default=str, sort_keys=True)
                dedupe_key = f"RUL_CommissionSlab|{slab_json}"
                if dedupe_key in dedupe_keys:
                    duplicate_rows += 1
                    continue
                dedupe_keys.add(dedupe_key)
                db.add(
                    ETL_StagingRawData(
                        batch_guid=batch_guid,
                        company_id=company_id,
                        table_name="RUL_CommissionSlab",
                        column_name="row_data",
                        source_row_number=idx + 2,
                        source_column_name="",
                        source_value=slab_json,
                        target_field="",
                        stored_value=slab_json,
                        validation_status="PENDING",
                        import_datetime=datetime.utcnow(),
                    )
                )
                staged_rows += 1

    batch.total_rows = staged_rows
    batch.import_status = "STAGED"
    db.commit()

    return {
        "message": "Upload successful",
        "batch_guid": batch_guid,
        "file_name": file_name,
        "file_hash": file_hash,
        "table_name": table_name,
        "workbook_fingerprint": workbook_fingerprint,
        "template_id": template.template_id,
        "sheet_name": template.sheet_name,
        "staged_rows": staged_rows,
        "deduplicated_rows": duplicate_rows,
    }


def _extract_natural_key(table_name: str, row: dict[str, Any]) -> dict[str, Any]:
    candidates = {
        "MST_Connector": ["connector_code", "pan"],
        "MST_Lender": ["pan", "lender_code"],
        "TRN_Case": ["case_number"],
    }
    key: dict[str, Any] = {}
    for field in candidates.get(table_name, []):
        val = _pick(row, field)
        if val not in (None, ""):
            key[field] = val
            break
    return key


def _existing_id_for_table(db: Session, table_name: str, natural_key: dict[str, Any], company_id: int) -> Optional[int]:
    if not natural_key:
        return None

    if table_name == "MST_Connector":
        query = db.query(MST_Connector).filter(MST_Connector.company_id == company_id)
        if "connector_code" in natural_key:
            rec = query.filter(MST_Connector.connector_code == str(natural_key["connector_code"])) .first()
            return rec.connector_id if rec else None
        if "pan" in natural_key:
            rec = query.filter(MST_Connector.pan == str(natural_key["pan"])) .first()
            return rec.connector_id if rec else None
        return None

    if table_name == "MST_Lender":
        query = db.query(MST_Lender).filter(MST_Lender.company_id == company_id)
        if "pan" in natural_key:
            rec = query.filter(MST_Lender.pan == str(natural_key["pan"])) .first()
            return rec.lender_id if rec else None
        if "lender_code" in natural_key:
            rec = query.filter(MST_Lender.lender_code == str(natural_key["lender_code"])) .first()
            return rec.lender_id if rec else None
        return None

    if table_name == "TRN_Case":
        case_number = natural_key.get("case_number")
        if case_number:
            rec = (
                db.query(TRN_Case)
                .filter(TRN_Case.case_number == str(case_number))
                .filter(TRN_Case.company_id == company_id)
                .first()
            )
            return rec.case_id if rec else None
    return None


def _natural_key_from_template(db: Session, template_id: Optional[int], row: dict[str, Any], table_name: str) -> dict[str, Any]:
    if not template_id:
        return _extract_natural_key(table_name, row)

    mappings = (
        db.query(META_FieldMapping)
        .filter(META_FieldMapping.template_id == template_id)
        .filter(META_FieldMapping.target_table == table_name)
        .filter(META_FieldMapping.is_natural_key == True)
        .all()
    )
    natural_key: dict[str, Any] = {}
    lowered = {_norm_col(str(k)): v for k, v in row.items()}
    for m in mappings:
        src = _norm_col(m.source_column)
        target = m.target_field
        if src in lowered and lowered[src] not in (None, ""):
            natural_key[target] = lowered[src]

    if natural_key:
        return natural_key
    return _extract_natural_key(table_name, row)


def _validate_pending_rows(db: Session, batch_guid: str) -> dict[str, int]:
    pending = (
        db.query(ETL_StagingRawData)
        .filter(ETL_StagingRawData.batch_guid == batch_guid)
        .filter(ETL_StagingRawData.validation_status == "PENDING")
        .all()
    )
    if not pending:
        return {"pending": 0, "passed": 0, "failed": 0, "warnings": 0}

    passed = 0
    failed = 0
    warnings = 0
    for rec in pending:
        row = _loads_row(rec.stored_value)
        if not row:
            rec.validation_status = "FAILED"
            failed += 1
            db.add(
                ETL_ErrorLog(
                    batch_guid=rec.batch_guid,
                    company_id=rec.company_id,
                    table_name=rec.table_name,
                    row_number=rec.source_row_number,
                    column_name=rec.column_name,
                    error_type="VALIDATION",
                    error_message="Empty or invalid row data",
                    error_datetime=datetime.utcnow(),
                )
            )
            continue

        result = execute_validation_rules(
            RuleExecutionRequest(table_name=rec.table_name, row_data=row, rule_ids=[]),
            db,
        )
        if result.passed:
            rec.validation_status = "PASSED"
            passed += 1
        else:
            rec.validation_status = "FAILED"
            failed += 1
            for msg in result.errors:
                db.add(
                    ETL_ErrorLog(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        table_name=rec.table_name,
                        row_number=rec.source_row_number,
                        column_name=rec.column_name,
                        error_type="VALIDATION",
                        error_message=msg,
                        error_datetime=datetime.utcnow(),
                    )
                )

        for warn in result.warnings:
            warnings += 1
            db.add(
                ETL_ErrorLog(
                    batch_guid=rec.batch_guid,
                    company_id=rec.company_id,
                    table_name=rec.table_name,
                    row_number=rec.source_row_number,
                    column_name=rec.column_name,
                    error_type="WARNING",
                    error_message=warn,
                    error_datetime=datetime.utcnow(),
                )
            )

    db.commit()
    return {"pending": len(pending), "passed": passed, "failed": failed, "warnings": warnings}


def _upsert_connector(db: Session, row: dict[str, Any], existing_id: Optional[int], company_id: int) -> int:
    if existing_id:
        rec = (
            db.query(MST_Connector)
            .filter(MST_Connector.connector_id == existing_id)
            .filter(MST_Connector.company_id == company_id)
            .first()
        )
        if rec:
            rec.full_name = str(_pick(row, "full_name", "connector_name", "connector name", default=rec.full_name))
            rec.pan = _pick(row, "pan", default=rec.pan)
            rec.gstin = _pick(row, "gstin", default=rec.gstin)
            rec.bank_name = _pick(row, "bank_name", "bank name", default=rec.bank_name)
            rec.account_number = _pick(row, "account_number", "account number", default=rec.account_number)
            rec.ifsc = _pick(row, "ifsc", default=rec.ifsc)
            rec.is_active = True
            db.add(rec)
            db.flush()
            return rec.connector_id

    rec = MST_Connector(
        connector_code=str(_pick(row, "connector_code", "connector code", default=f"AUTO-{uuid.uuid4().hex[:8]}")),
        full_name=str(_pick(row, "full_name", "connector_name", "connector name", default="Unknown Connector")),
        pan=_pick(row, "pan"),
        gstin=_pick(row, "gstin"),
        bank_name=_pick(row, "bank_name", "bank name"),
        account_number=_pick(row, "account_number", "account number"),
        ifsc=_pick(row, "ifsc"),
        is_active=True,
        company_id=company_id,
    )
    db.add(rec)
    db.flush()
    return rec.connector_id


def _upsert_lender(db: Session, row: dict[str, Any], existing_id: Optional[int], company_id: int) -> int:
    if existing_id:
        rec = (
            db.query(MST_Lender)
            .filter(MST_Lender.lender_id == existing_id)
            .filter(MST_Lender.company_id == company_id)
            .first()
        )
        if rec:
            rec.lender_name = str(_pick(row, "lender_name", "lender name", default=rec.lender_name))
            rec.gstin = _pick(row, "gstin", default=rec.gstin)
            rec.lender_code = str(_pick(row, "lender_code", "lender code", default=rec.lender_code or f"L-{uuid.uuid4().hex[:8]}"))
            rec.is_nbfc = bool(_pick(row, "is_nbfc", "is nbfc", default=rec.is_nbfc))
            rec.is_active = True
            db.add(rec)
            db.flush()
            return rec.lender_id

    rec = MST_Lender(
        lender_name=str(_pick(row, "lender_name", "lender name", default="Unknown Lender")),
        pan=str(_pick(row, "pan", default=f"PAN-{uuid.uuid4().hex[:8]}")),
        gstin=_pick(row, "gstin"),
        lender_code=str(_pick(row, "lender_code", "lender code", default=f"L-{uuid.uuid4().hex[:8]}")),
        is_nbfc=bool(_pick(row, "is_nbfc", "is nbfc", default=False)),
        is_active=True,
        company_id=company_id,
    )
    db.add(rec)
    db.flush()
    return rec.lender_id


def _upsert_case(db: Session, row: dict[str, Any], existing_id: Optional[int], company_id: int) -> int:
    if existing_id:
        rec = (
            db.query(TRN_Case)
            .filter(TRN_Case.case_id == existing_id)
            .filter(TRN_Case.company_id == company_id)
            .first()
        )
        if rec:
            rec.customer_id = int(_pick(row, "customer_id", "customer id", default=rec.customer_id))
            rec.lender_id = int(_pick(row, "lender_id", "lender id", default=rec.lender_id))
            rec.product_id = int(_pick(row, "product_id", "product id", default=rec.product_id))
            rec.sanction_amount = _to_float(
                _pick(row, "sanction_amount", "sanction amount", default=rec.sanction_amount or 0),
                default=0.0,
            )
            rec.disbursement_amount = _to_float(
                _pick(row, "disbursement_amount", "disbursement amount", default=rec.disbursement_amount or 0),
                default=0.0,
            )
            rec.status = str(_pick(row, "status", default=rec.status or "LEAD"))
            rec.is_active = True
            db.add(rec)
            db.flush()
            return rec.case_id

    rec = TRN_Case(
        case_number=str(_pick(row, "case_number", "case number", default=f"CASE-{uuid.uuid4().hex[:8]}")),
        customer_id=int(_pick(row, "customer_id", "customer id", default=1)),
        lender_id=int(_pick(row, "lender_id", "lender id", default=1)),
        product_id=int(_pick(row, "product_id", "product id", default=1)),
        sanction_amount=_to_float(_pick(row, "sanction_amount", "sanction amount", default=0), default=0.0),
        disbursement_amount=_to_float(_pick(row, "disbursement_amount", "disbursement amount", default=0), default=0.0),
        status=str(_pick(row, "status", default="LEAD")),
        is_active=True,
        company_id=company_id,
    )
    db.add(rec)
    db.flush()
    return rec.case_id


@router.post("/upload")
async def upload_to_staging(
    file: UploadFile = File(...),
    entity_type: str = Form(...),
    company_id: Optional[int] = Form(None),
    auto_process: Optional[str] = Form("true"),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    effective_company_id = current_user.company_id
    if company_id is not None and company_id != effective_company_id:
        raise HTTPException(status_code=403, detail="Cross-tenant upload is not allowed")
    file_bytes = await file.read()
    result = upload_to_staging_bytes(file_bytes, file.filename or "", entity_type, effective_company_id, db)

    if isinstance(result, dict) and result.get("status_code") == 202:
        return {
            "status": "mapping_required",
            "mode": "dynamic_mapping",
            "file_name": file.filename or "",
            "entity_type": entity_type,
            **result,
        }
    if isinstance(result, dict) and result.get("status_code") in {400, 409, 422}:
        return JSONResponse(
            status_code=int(result["status_code"]),
            content={
                "status": "upload_failed",
                **_json_safe(result),
            },
        )

    if not _to_bool_form(auto_process, default=True):
        return {
            "status": "staged",
            "mode": "strict_template",
            **result,
        }

    batch_guid = result["batch_guid"]
    try:
        promotion = promote_staged_data(
            batch_guid=batch_guid,
            conflict_resolution=None,
            current_user=current_user,
            db=db,
        )
    except HTTPException as exc:
        validation_errors = (
            db.query(ETL_ErrorLog)
            .filter(ETL_ErrorLog.batch_guid == batch_guid)
            .filter(ETL_ErrorLog.company_id == current_user.company_id)
            .order_by(ETL_ErrorLog.error_datetime.desc())
            .limit(100)
            .all()
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "validation_failed" if exc.status_code == 400 else "promotion_failed",
                "mode": "strict_template",
                "batch_guid": batch_guid,
                "upload": _json_safe(result),
                "detail": _json_safe(exc.detail),
                "errors": _json_safe(validation_errors),
            },
        )

    return {
        "status": "success",
        "mode": "strict_template",
        "batch_guid": batch_guid,
        "upload": result,
        "promotion": promotion,
    }


@router.get("/template")
def resolve_template(
    fingerprint: Optional[str] = None,
    file_name: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    template = None
    resolution = "none"
    if fingerprint:
        template = get_template_by_fingerprint(db, fingerprint, company_id=current_user.company_id)
        if template:
            resolution = "fingerprint"
    if template is None and file_name:
        template = get_template_by_pattern(db, file_name, company_id=current_user.company_id)
        if template:
            resolution = "pattern"

    if template is None:
        return {"found": False, "resolution": resolution}

    return {
        "found": True,
        "resolution": resolution,
        "template": {
            "template_id": template.template_id,
            "template_name": template.template_name,
            "sheet_name": template.sheet_name,
            "status": template.status,
            "conflict_resolution": template.conflict_resolution,
            "shared": bool(template.shared),
        },
    }


@router.post("/template/detect")
async def detect_template(
    file: UploadFile = File(...),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    file_bytes = await file.read()
    analysis = analyze_excel_bytes(file_bytes, sheet_name=None, header_row=1)
    fingerprint = analysis.get("workbook_fingerprint")
    file_name = file.filename or ""
    resolution = resolve_template(
        fingerprint=fingerprint,
        file_name=file_name,
        current_user=current_user,
        db=db,
    )
    return {
        "file_name": file_name,
        "workbook_fingerprint": fingerprint,
        "resolution": resolution,
    }


@router.post("/stage")
async def stage_only(
    file: UploadFile = File(...),
    entity_type: str = Form(...),
    company_id: Optional[int] = Form(None),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    effective_company_id = current_user.company_id
    if company_id is not None and company_id != effective_company_id:
        raise HTTPException(status_code=403, detail="Cross-tenant upload is not allowed")
    file_bytes = await file.read()
    result = upload_to_staging_bytes(file_bytes, file.filename or "", entity_type, effective_company_id, db)
    if isinstance(result, dict) and result.get("status_code"):
        return JSONResponse(status_code=int(result["status_code"]), content=_json_safe(result))
    return {"status": "staged", **result}


@router.post("/validate")
def validate_batch(
    batch_guid: str = Form(...),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    batch = (
        db.query(ETL_ImportBatch)
        .filter(ETL_ImportBatch.batch_guid == batch_guid)
        .filter(ETL_ImportBatch.company_id == current_user.company_id)
        .first()
    )
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    summary = _validate_pending_rows(db, batch_guid)
    return {"batch_guid": batch_guid, "validation_summary": summary}


@router.get("/batches")
def list_batches(current_user: SEC_User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(ETL_ImportBatch).filter(ETL_ImportBatch.company_id == current_user.company_id)
    batches = query.order_by(ETL_ImportBatch.import_datetime.desc()).all()
    return batches


@router.get("/staging")
def list_staging(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_StagingRawData.batch_guid == batch_guid)
    records = query.order_by(ETL_StagingRawData.staging_id.desc()).all()
    return {"total_records": len(records), "records": records}


@router.get("/staging/connectors")
def get_staged_connectors(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.table_name == "MST_Connector")
    query = query.filter(ETL_StagingRawData.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_StagingRawData.batch_guid == batch_guid)
    records = query.all()
    return {"total_records": len(records), "records": records}


@router.get("/staging/lenders")
def get_staged_lenders(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.table_name == "MST_Lender")
    query = query.filter(ETL_StagingRawData.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_StagingRawData.batch_guid == batch_guid)
    records = query.all()
    return {"total_records": len(records), "records": records}


@router.get("/staging/cases")
def get_staged_cases(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_StagingRawData).filter(ETL_StagingRawData.table_name == "TRN_Case")
    query = query.filter(ETL_StagingRawData.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_StagingRawData.batch_guid == batch_guid)
    records = query.all()
    return {"total_records": len(records), "records": records}


@router.get("/errors")
def get_etl_errors(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_ErrorLog).filter(ETL_ErrorLog.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_ErrorLog.batch_guid == batch_guid)
    return query.order_by(ETL_ErrorLog.error_datetime.desc()).all()


@router.get("/lineage")
def get_etl_lineage(
    batch_guid: Optional[str] = None,
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(ETL_DataLineage).filter(ETL_DataLineage.company_id == current_user.company_id)
    if batch_guid:
        query = query.filter(ETL_DataLineage.batch_guid == batch_guid)
    rows = query.order_by(ETL_DataLineage.lineage_id.desc()).all()
    return {"total_records": len(rows), "records": rows}


@router.post("/promote")
def promote_staged_data(
    batch_guid: str = Form(...),
    conflict_resolution: Optional[str] = Form(None),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    batch_query = db.query(ETL_ImportBatch).filter(ETL_ImportBatch.batch_guid == batch_guid)
    batch_query = batch_query.filter(ETL_ImportBatch.company_id == current_user.company_id)
    batch = batch_query.first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Enforce validation as part of promotion so the workflow remains end-to-end operational.
    validation_summary = _validate_pending_rows(db, batch_guid)

    template = None
    policy = (conflict_resolution or "").upper().strip() if conflict_resolution else None
    if batch.template_id:
        template = (
            db.query(META_ImportTemplate)
            .filter(META_ImportTemplate.template_id == batch.template_id)
            .filter((META_ImportTemplate.company_id == current_user.company_id) | (META_ImportTemplate.shared == True))
            .first()
        )
    if template is None and batch.file_name:
        template = get_template_by_pattern(db, batch.file_name, company_id=current_user.company_id)
    if template and template.status == "Active":
        if not policy:
            policy = str(template.conflict_resolution or "SKIP").upper()
    policy = policy or "SKIP"

    if template:
        try:
            mapping_definition = json.loads(template.mapping_definition or "{}")
        except Exception:
            mapping_definition = {}
        if supports_multi_target(mapping_definition.get("mappings", [])):
            result = promote_batch(db, batch_guid, policy)
            if result.get("error"):
                raise HTTPException(
                    status_code=409,
                    detail={
                        "message": result["error"],
                        "batch_guid": batch_guid,
                        "results": result.get("results", {}),
                        "summary": result.get("summary", {}),
                        "validation_summary": validation_summary,
                    },
                )
            result["validation_summary"] = validation_summary
            return result

    records = (
        db.query(ETL_StagingRawData)
        .filter(ETL_StagingRawData.batch_guid == batch_guid)
        .filter(ETL_StagingRawData.validation_status == "PASSED")
        .filter(ETL_StagingRawData.is_promoted == False)
        .all()
    )
    if not records:
        raise HTTPException(status_code=400, detail="No eligible staged records for this batch")

    promoted = 0
    skipped = 0
    seen_slab_labels: set[str] = set()
    for rec in records:
        row = _loads_row(rec.stored_value)
        try:
            rule_result = execute_validation_rules(
                RuleExecutionRequest(table_name=rec.table_name, row_data=row, rule_ids=[]),
                db,
            )
            if not rule_result.passed:
                rec.validation_status = "FAILED"
                db.add(
                    ETL_ErrorLog(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        table_name=rec.table_name,
                        row_number=rec.source_row_number,
                        column_name=rec.column_name,
                        error_type="VALIDATION",
                        error_message="; ".join(rule_result.errors),
                        error_datetime=datetime.utcnow(),
                    )
                )
                continue

            target_id: Optional[int] = None
            natural_key = _natural_key_from_template(db, template.template_id if template else None, row, rec.table_name)
            existing_id = _existing_id_for_table(db, rec.table_name, natural_key, current_user.company_id)

            if existing_id and policy == "FAIL":
                rec.validation_status = "FAILED"
                db.add(
                    ETL_ErrorLog(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        table_name=rec.table_name,
                        row_number=rec.source_row_number,
                        column_name=rec.column_name,
                        error_type="DUPLICATE",
                        error_message=f"Duplicate record exists for natural key: {natural_key}",
                        error_datetime=datetime.utcnow(),
                    )
                )
                continue

            if existing_id and policy == "SKIP":
                rec.is_promoted = True
                skipped += 1
                db.add(
                    ETL_DataLineage(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        staging_id=rec.staging_id,
                        target_table=rec.table_name,
                        target_id=existing_id,
                        created_at=datetime.utcnow(),
                    )
                )
                continue

            if rec.table_name == "MST_Connector":
                target_id = _upsert_connector(db, row, existing_id if policy == "UPDATE" else None, current_user.company_id)
            elif rec.table_name == "MST_Lender":
                target_id = _upsert_lender(db, row, existing_id if policy == "UPDATE" else None, current_user.company_id)
            elif rec.table_name == "TRN_Case":
                target_id = _upsert_case(db, row, existing_id if policy == "UPDATE" else None, current_user.company_id)
                if not existing_id:
                    revenue_base = _to_float(_pick(row, "sanction_amount", "sanction amount", default=0), default=0.0)
                    revenue_amount = revenue_base * 0.02
                    db.add(
                        TRN_Revenue(
                            company_id=current_user.company_id,
                            case_id=target_id,
                            revenue_date=datetime.utcnow().date(),
                            base_revenue_amount=revenue_amount,
                            gst_amount=0,
                            tds_amount=0,
                            net_amount=revenue_amount,
                            payment_status="PENDING",
                            is_active=True,
                        )
                    )
                    db.add(
                        TRN_Commission(
                            company_id=current_user.company_id,
                            case_id=target_id,
                            connector_id=int(_pick(row, "connector_id", "connector id", default=1)),
                            commission_date=datetime.utcnow().date(),
                            base_commission_amount=revenue_amount / 2,
                            gross_commission_amount=revenue_amount / 2,
                            net_amount=revenue_amount / 2,
                            payment_status="PENDING",
                            is_active=True,
                        )
                    )
            elif rec.table_name == "RUL_CommissionSlab":
                slab_label = str(_pick(row, "slab_label", "label", default="Unknown Slab"))
                slab_rate = _to_float(_pick(row, "rate", default=0.0), default=0.0)
                existing_slab = (
                    db.query(RUL_CommissionSlab)
                    .filter(RUL_CommissionSlab.slab_label == slab_label)
                    .first()
                )
                if existing_slab:
                    existing_slab.rate = slab_rate
                    existing_slab.is_active = True
                elif slab_label not in seen_slab_labels:
                    seen_slab_labels.add(slab_label)
                    slab = RUL_CommissionSlab(slab_label=slab_label, rate=slab_rate, is_active=True)
                    db.add(slab)
                    db.flush()
                    target_id = slab.slab_id

            if target_id is not None:
                db.add(
                    ETL_DataLineage(
                        batch_guid=rec.batch_guid,
                        company_id=rec.company_id,
                        staging_id=rec.staging_id,
                        target_table=rec.table_name,
                        target_id=target_id,
                        created_at=datetime.utcnow(),
                    )
                )

            rec.validation_status = "PASSED"
            rec.is_promoted = True
            promoted += 1
        except Exception as exc:
            rec.validation_status = "FAILED"
            db.add(
                ETL_ErrorLog(
                    batch_guid=rec.batch_guid,
                    company_id=rec.company_id,
                    table_name=rec.table_name,
                    row_number=rec.source_row_number,
                    column_name=rec.column_name,
                    error_type="PROMOTION",
                    error_message=str(exc),
                    error_datetime=datetime.utcnow(),
                )
            )

    batch.successful_rows += promoted
    batch.failed_rows = max(batch.total_rows - batch.successful_rows - skipped, 0)
    batch.import_status = "PROMOTED" if promoted and batch.failed_rows == 0 else ("PARTIAL" if promoted else "FAILED")
    batch.is_complete = True
    db.commit()

    return {
        "message": "Promotion completed",
        "batch_guid": batch_guid,
        "promoted_count": promoted,
        "skipped_count": skipped,
        "conflict_resolution": policy,
        "validation_summary": validation_summary,
    }