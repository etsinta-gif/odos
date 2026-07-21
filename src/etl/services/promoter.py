import json
import re
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from src.etl.handlers.registry import get_handler, get_tables_in_order
from src.metadata.models import META_ImportTemplate
from src.transactions.models import ETL_DataLineage, ETL_ErrorLog, ETL_ImportBatch, ETL_StagingRawData


SUPPORTED_MULTI_TARGET_TABLES = {
    "MST_Lender",
    "MST_Product",
    "MST_Connector",
    "MST_ConnectorBank",
    "MST_Employee",
    "MST_EmployeeBankAccount",
    "MST_Vendor",
    "REF_ExpenseCategory",
    "RUL_CommissionRule",
    "RUL_CommissionSlab",
    "RUL_Contest",
    "RUL_InternalIncentiveScheme",
    "TRN_Case",
    "TRN_Revenue",
    "TRN_Commission",
    "TRN_CaseConnectorSplit",
    "TRN_IncentiveEarned",
    "TRN_Invoice",
    "TRN_Salary",
    "TRN_StatutoryPayment",
    "TRN_Expense",
    "TRN_BankStatementLine",
}


def supports_multi_target(mappings: list[dict[str, Any]]) -> bool:
    mapped_tables = {str(m.get("target_table") or "").strip() for m in mappings if m.get("target_table")}
    return len(mapped_tables.intersection(SUPPORTED_MULTI_TARGET_TABLES)) > 1


def _norm_col(value: str) -> str:
    norm = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
    norm = re.sub(r"_+", "_", norm).strip("_")
    return norm


def _safe_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        import math

        num = float(str(value).replace("%", "").replace(",", "").replace("₹", "").replace("INR", "").strip())
        return num if math.isfinite(num) else None
    except Exception:
        return None


def _to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _tier_bounds(label: str) -> tuple[float | None, float | None]:
    text = str(label or "")
    if "<" in text and "50" in text and "L" in text:
        return 0.0, 5000000.0
    if "50" in text and "1 Cr" in text:
        return 5000000.0, 10000000.0
    if "1 Cr" in text and "2 Cr" in text:
        return 10000000.0, 20000000.0
    if "2 Cr" in text and "3 Cr" in text:
        return 20000000.0, 30000000.0
    if "3 Cr" in text and "5 Cr" in text:
        return 30000000.0, 50000000.0
    if "5 Cr" in text and "10 Cr" in text:
        return 50000000.0, 100000000.0
    if "10 Cr" in text and "25 Cr" in text:
        return 100000000.0, 250000000.0
    if "25 Cr" in text and "50 Cr" in text:
        return 250000000.0, 500000000.0
    if "50 Cr" in text and "100 Cr" in text:
        return 500000000.0, 1000000000.0
    if ">=" in text or "≥" in text:
        return 1000000000.0, None
    return None, None


def _common_fields(lowered: dict[str, Any]) -> dict[str, Any]:
    common: dict[str, Any] = {}
    alias_pairs = {
        "lender_code": ["dsa_code", "lender_code"],
        "lender_name": ["lender_nbfc", "lender_name"],
        "dsa_code": ["dsa_code"],
        "pan": ["pan"],
        "gstin": ["gstin"],
        "sub_product": ["sub_product"],
        "product_name": ["sub_product", "product_name"],
        "product_code": ["product_code"],
        "roi_percent": ["roi", "roi_percent"],
        "slab_type": ["slab_type"],
        "base_percent": ["base"],
        "headline_percent": ["headline"],
        "pf_percent": ["pf"],
        "i_percent": ["i"],
        "qualifying_condition": ["qualifying"],
        "qualifying_notes": ["qualifying_notes"],
        "commercial_terms": ["commercial"],
        "clawback_conditions": ["post_disbursement_clawback_conditions"],
        "frequency": ["contest_frequency", "frequency"],
        "target_amount": ["contest_target", "target_amount"],
        "bonus_percent": ["contest_bonus_percent", "bonus_percent"],
        "period": ["contest_period", "period"],
        "notes": ["contest_notes", "notes"],
        "is_nbfc": ["nbfc"],
    }
    for target_field, aliases in alias_pairs.items():
        for alias in aliases:
            if alias in lowered and lowered[alias] not in (None, ""):
                common[target_field] = lowered[alias]
                break
    common["is_nbfc"] = _to_bool(common.get("is_nbfc")) if "is_nbfc" in common else False
    if "roi_percent" in common:
        common["roi_percent"] = _to_float(common.get("roi_percent"))
    if "base_percent" in common:
        common["base_percent"] = _to_float(common.get("base_percent"))
    if "headline_percent" in common:
        common["headline_percent"] = _to_float(common.get("headline_percent"))
    if "pf_percent" in common:
        common["pf_percent"] = _to_float(common.get("pf_percent"))
    if "i_percent" in common:
        common["i_percent"] = _to_float(common.get("i_percent"))
    if "target_amount" in common:
        common["target_amount"] = _to_float(common.get("target_amount"))
    if "bonus_percent" in common:
        common["bonus_percent"] = _to_float(common.get("bonus_percent"))
    return common


def _build_table_rows(template: META_ImportTemplate, staging_rows: list[ETL_StagingRawData]) -> dict[str, list[dict[str, Any]]]:
    mapping_definition = _safe_json(template.mapping_definition)
    mappings = mapping_definition.get("mappings", [])
    normalized_mappings: dict[str, list[dict[str, Any]]] = {}
    slab_mappings: list[dict[str, Any]] = []

    for mapping in mappings:
        target_table = str(mapping.get("target_table") or "").strip()
        source_column = str(mapping.get("source_column") or "").strip()
        target_field = str(mapping.get("target_field") or "").strip()
        if not target_table or not source_column or not target_field:
            continue
        if target_table == "RUL_CommissionSlab":
            slab_mappings.append(mapping)
        elif target_table in SUPPORTED_MULTI_TARGET_TABLES:
            normalized_mappings.setdefault(target_table, []).append(mapping)

    table_rows: dict[str, list[dict[str, Any]]] = {table: [] for table in get_tables_in_order()}

    for staging_row in staging_rows:
        raw = _safe_json(staging_row.source_value or staging_row.stored_value)
        lowered = {_norm_col(key): value for key, value in raw.items()}
        common = _common_fields(lowered)

        for table_name, table_mappings in normalized_mappings.items():
            mapped_data = dict(common)
            for mapping in table_mappings:
                src = _norm_col(str(mapping.get("source_column") or ""))
                target = str(mapping.get("target_field") or "").strip()
                if src in lowered:
                    mapped_data[target] = lowered[src]

            if table_name == "MST_Product":
                if mapped_data.get("product_name") in (None, "") and mapped_data.get("sub_product") not in (None, ""):
                    mapped_data["product_name"] = mapped_data["sub_product"]
                mapped_data["roi_percent"] = _to_float(mapped_data.get("roi_percent"))
            elif table_name == "RUL_CommissionRule":
                mapped_data["base_percent"] = _to_float(mapped_data.get("base_percent"))
                mapped_data["headline_percent"] = _to_float(mapped_data.get("headline_percent"))
                mapped_data["pf_percent"] = _to_float(mapped_data.get("pf_percent"))
                mapped_data["i_percent"] = _to_float(mapped_data.get("i_percent"))
                if mapped_data.get("base_percent") is not None and mapped_data.get("base_rate") is None:
                    mapped_data["base_rate"] = mapped_data["base_percent"]
                if mapped_data.get("headline_percent") is not None and mapped_data.get("flat_rate") is None:
                    mapped_data["flat_rate"] = mapped_data["headline_percent"]

            if any(value not in (None, "") for value in mapped_data.values()):
                table_rows[table_name].append({"staging_row": staging_row, "mapped_data": mapped_data})

        slab_common = dict(common)
        slab_common["slab_type"] = slab_common.get("slab_type") or "FLAT"
        for mapping in slab_mappings:
            src = _norm_col(str(mapping.get("source_column") or ""))
            if src not in lowered:
                continue
            rate = _to_float(lowered[src])
            if rate is None:
                continue
            tier_name = str(mapping.get("source_column") or "")
            tier_min, tier_max = _tier_bounds(tier_name)
            mapped_data = dict(slab_common)
            mapped_data.update(
                {
                    "slab_label": tier_name,
                    "tier_name": tier_name,
                    "tier_min": tier_min,
                    "tier_max": tier_max,
                    "rate": rate,
                }
            )
            table_rows["RUL_CommissionSlab"].append({"staging_row": staging_row, "mapped_data": mapped_data})

    return table_rows


def promote_batch(db: Session, batch_guid: str, conflict_resolution: str = "SKIP") -> dict[str, Any]:
    batch = db.query(ETL_ImportBatch).filter(ETL_ImportBatch.batch_guid == batch_guid).first()
    if batch is None:
        return {"error": "Batch not found"}
    if batch.template_id is None:
        return {"error": "Batch template_id is not set"}

    template = (
        db.query(META_ImportTemplate)
        .filter(META_ImportTemplate.template_id == batch.template_id)
        .filter(META_ImportTemplate.status == "Active")
        .first()
    )
    if template is None:
        return {"error": "Active template not found for this batch"}

    staging_rows = (
        db.query(ETL_StagingRawData)
        .filter(ETL_StagingRawData.batch_guid == batch_guid)
        .filter(ETL_StagingRawData.validation_status == "PASSED")
        .filter(ETL_StagingRawData.is_promoted == False)
        .all()
    )
    if not staging_rows:
        return {"error": "No eligible rows to promote"}

    table_rows = _build_table_rows(template, staging_rows)
    results: dict[str, Any] = {}

    for table_name in get_tables_in_order():
        rows_for_table = table_rows.get(table_name) or []
        if not rows_for_table:
            continue
        handler_info = get_handler(table_name)
        if handler_info is None:
            continue
        try:
            result = handler_info["handler"](db, rows_for_table, template, conflict_resolution)
            results[table_name] = {
                "created": result.get("created", 0),
                "updated": result.get("updated", 0),
                "skipped": result.get("skipped", 0),
                "failed": result.get("failed", 0),
            }
            for row_wrapper, target_id in result.get("records", []):
                staging_row = row_wrapper["staging_row"]
                db.add(
                    ETL_DataLineage(
                        batch_guid=batch_guid,
                        company_id=staging_row.company_id,
                        staging_id=staging_row.staging_id,
                        target_table=table_name,
                        target_id=target_id,
                        created_at=datetime.utcnow(),
                    )
                )
        except Exception as exc:
            results[table_name] = {"created": 0, "updated": 0, "skipped": 0, "failed": len(rows_for_table), "error": str(exc)}
            for item in rows_for_table:
                staging_row = item["staging_row"]
                db.add(
                    ETL_ErrorLog(
                        batch_guid=batch_guid,
                        company_id=staging_row.company_id,
                        table_name=table_name,
                        row_number=staging_row.source_row_number,
                        column_name=staging_row.column_name,
                        error_type="PROMOTION",
                        error_message=str(exc),
                        error_datetime=datetime.utcnow(),
                    )
                )

    for row in staging_rows:
        row.is_promoted = True

    total_written = sum(result.get("created", 0) + result.get("updated", 0) for result in results.values())
    total_failed = sum(result.get("failed", 0) for result in results.values())
    has_target_failures = total_failed > 0
    batch.successful_rows += total_written
    batch.failed_rows = total_failed
    batch.import_status = "PROMOTED" if total_written and total_failed == 0 else ("PARTIAL" if total_written else "FAILED")
    batch.is_complete = True
    db.commit()

    response: dict[str, Any] = {
        "batch_guid": batch_guid,
        "template_id": batch.template_id,
        "results": results,
        "message": "Promotion completed",
        "summary": {
            "total_created_or_updated": total_written,
            "total_failed": total_failed,
            "has_target_failures": has_target_failures,
        },
    }
    if has_target_failures:
        response["error"] = f"Promotion completed with {total_failed} sub-target failures"
    return response
