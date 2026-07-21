import json
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from scripts.validate_staging import validate_staging
from src.core.database import SessionLocal
from src.transactions.models import ETL_ErrorLog


def pick_entity_type(file_name: str) -> str:
    n = file_name.lower()
    if "connector" in n:
        return "MST_Connector"
    if "lender" in n or "payout" in n:
        return "MST_Lender"
    if "tracker" in n or "dsr" in n:
        return "TRN_Case"
    if "salary" in n:
        return "TRN_Case"
    return "MST_Lender"


def pick_sheet(file_path: Path) -> str:
    xls = pd.ExcelFile(file_path)
    sheets = [str(s) for s in xls.sheet_names]
    for candidate in ["Master", "MASTER", "Sheet1"]:
        if candidate in sheets:
            return candidate
    return sheets[0]


def allowed_target_tables(entity_type: str) -> set[str]:
    if entity_type == "MST_Lender":
        return {"MST_Lender", "MST_Product", "RUL_CommissionRule", "RUL_CommissionSlab"}
    if entity_type == "MST_Connector":
        return {"MST_Connector"}
    if entity_type == "TRN_Case":
        return {"TRN_Case"}
    return {entity_type}


def build_mappings(columns: list[dict], entity_type: str) -> tuple[list[dict], int]:
    mappings = []
    ignored = 0
    allowed_tables = allowed_target_tables(entity_type)
    connector_allowed_fields = {"connector_code", "full_name", "pan", "gstin", "bank_name", "account_number", "ifsc"}
    for c in columns:
        tgt_t = c.get("suggested_target_table")
        tgt_f = c.get("suggested_target_field")
        if c.get("ignore") or not tgt_t or not tgt_f or tgt_t not in allowed_tables:
            ignored += 1
            continue

        if entity_type == "MST_Connector":
            target_field = str(tgt_f).strip().lower()
            source_name = str(c.get("source_column") or "").strip().lower()
            pattern = str(c.get("pattern") or "").strip().lower()
            if target_field not in connector_allowed_fields:
                ignored += 1
                continue
            if target_field == "pan" and "pan" not in source_name and pattern != "pan":
                ignored += 1
                continue

        src_norm = str(c.get("source_column", "")).strip().lower()
        mappings.append(
            {
                "source_column": c.get("source_column"),
                "target_table": tgt_t,
                "target_field": tgt_f,
                "confidence_score": int(c.get("confidence_score") or 0),
                "is_verified": True,
                "is_natural_key": src_norm in {"pan", "lender_code", "connector_code", "registration_id", "case_number", "dsa code"},
                "notes": c.get("notes"),
            }
        )
    return mappings, ignored


def summarize_promotion_results(promote_body: dict) -> tuple[int, int, int, int]:
    results = promote_body.get("results") or {}
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    for _, counters in results.items():
        created += int(counters.get("created") or 0)
        updated += int(counters.get("updated") or 0)
        skipped += int(counters.get("skipped") or 0)
        failed += int(counters.get("failed") or 0)
    return created, updated, skipped, failed


def classify_result(promote_status: int, promote_body: dict, staged_rows: int, error_count: int) -> str:
    if promote_status != 200:
        detail = (promote_body or {}).get("detail")
        if isinstance(detail, str) and "No eligible rows to promote" in detail:
            return "FAIL_VALIDATION"
        return "FAIL"

    created, updated, skipped, failed = summarize_promotion_results(promote_body)
    success_rows = created + updated

    if staged_rows > 0 and success_rows == 0 and failed > 0:
        return "FAIL"

    if error_count > 0 and success_rows == 0:
        return "FAIL"

    if failed > 0 and success_rows > 0:
        return "PARTIAL"

    return "PASS"


def write_markdown_report(report: dict, out_path: Path) -> None:
    results = report.get("results") or []
    pass_count = sum(1 for r in results if r.get("result") == "PASS")
    pass_ignore_count = sum(1 for r in results if r.get("result") == "PASS_IGNORE")
    partial_count = sum(1 for r in results if r.get("result") == "PARTIAL")
    fail_count = sum(1 for r in results if str(r.get("result", "")).startswith("FAIL"))

    lines = []
    lines.append("# FCPL Pilot Report (Folder Run)")
    lines.append("")
    lines.append(f"- Root Folder: {report.get('root')}")
    lines.append(f"- Files Tested: {report.get('file_count', 0)}")
    lines.append(f"- PASS: {pass_count}")
    lines.append(f"- PASS_IGNORE: {pass_ignore_count}")
    lines.append(f"- PARTIAL: {partial_count}")
    lines.append(f"- FAIL*: {fail_count}")
    lines.append("")
    lines.append("## Per-File Outcome")
    lines.append("")
    lines.append("| File | Result | Sheet | Mapped | Ignored | Upload | Promote | Error Count |")
    lines.append("|---|---:|---|---:|---:|---:|---:|---:|")
    for r in results:
        lines.append(
            "| {name} | {result} | {sheet} | {mapped} | {ignored} | {upload} | {promote} | {errors} |".format(
                name=r.get("name", ""),
                result=r.get("result", ""),
                sheet=r.get("sheet", ""),
                mapped=r.get("mapped_columns", ""),
                ignored=r.get("ignored_columns", ""),
                upload=r.get("upload_status", ""),
                promote=r.get("promote_status", ""),
                errors=r.get("error_count", 0),
            )
        )

    lines.append("")
    lines.append("## Failure/Partial Details")
    lines.append("")
    for r in results:
        outcome = str(r.get("result", ""))
        if outcome == "PASS" or outcome == "PASS_IGNORE":
            continue
        lines.append(f"### {r.get('name')}")
        lines.append(f"- Result: {outcome}")
        lines.append(f"- Notes: {'; '.join(r.get('notes') or []) if r.get('notes') else '-'}")
        pb = r.get("promote_body") or {}
        if pb:
            lines.append(f"- Promote Response: {json.dumps(pb)}")
        es = r.get("error_sample") or []
        if es:
            lines.append("- Error Samples:")
            for e in es[:5]:
                lines.append(
                    f"  - [{e.get('type')}] {e.get('table')}: {e.get('message')}"
                )
        lines.append("")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> dict:
    root = Path(r"C:\Users\etsin\Desktop\1infinity\FinOps - Old Data\Master Data Sheets - For Suresh CFO")
    client = TestClient(app)

    files = sorted([p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".xlsx", ".xls", ".xlsm"}])

    report: dict = {"root": str(root), "file_count": len(files), "results": []}

    for fp in files:
        item = {
            "file": str(fp),
            "name": fp.name,
            "result": "UNKNOWN",
            "notes": [],
        }
        try:
            entity_type = pick_entity_type(fp.name)
            sheet = pick_sheet(fp)
            item["entity_type"] = entity_type
            item["sheet"] = sheet

            raw = fp.read_bytes()
            analyze = client.post(
                "/api/admin/mapping/analyze",
                files={"file": (fp.name, raw, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                data={"sheet_name": sheet, "header_row": "1"},
            )
            item["analyze_status"] = analyze.status_code
            if analyze.status_code != 200:
                item["result"] = "FAIL"
                item["notes"].append(f"analyze failed: {analyze.text[:200]}")
                report["results"].append(item)
                continue

            aj = analyze.json()
            sheets = aj.get("sheets") or []
            if not sheets:
                item["result"] = "FAIL"
                item["notes"].append("no sheets from analyze")
                report["results"].append(item)
                continue

            cols = sheets[0].get("columns", [])
            mappings, ignored = build_mappings(cols, entity_type)
            item["mapped_columns"] = len(mappings)
            item["ignored_columns"] = ignored

            if not mappings:
                item["result"] = "PASS_IGNORE"
                item["notes"].append("no relevant columns mapped")
                report["results"].append(item)
                continue

            analyze_all = client.post(
                "/api/admin/mapping/analyze",
                files={"file": (fp.name, raw, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                data={"header_row": "1"},
            )
            wb_fp = analyze_all.json().get("workbook_fingerprint") if analyze_all.status_code == 200 else None

            template_payload = {
                "template_name": f"Pilot FinOps {fp.stem}",
                "file_pattern": f".*{fp.name}.*",
                "fingerprint": wb_fp,
                "sheet_name": sheet,
                "header_row": 1,
                "conflict_resolution": "UPDATE",
                "mappings": mappings,
                "status": "Draft",
            }
            confirm = client.post("/api/admin/mapping/confirm", json=template_payload)
            item["template_create_status"] = confirm.status_code
            if confirm.status_code != 200:
                item["result"] = "FAIL"
                item["notes"].append(f"template confirm failed: {confirm.text[:200]}")
                report["results"].append(item)
                continue

            tid = confirm.json().get("template_id")
            item["template_id"] = tid
            item["template_approve_status"] = client.put(f"/api/admin/mapping/templates/{tid}", json={"status": "Approved"}).status_code
            item["template_active_status"] = client.put(f"/api/admin/mapping/templates/{tid}", json={"status": "Active"}).status_code

            upload = client.post(
                "/api/v1/etl/upload",
                files={"file": (fp.name, raw, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
                data={"entity_type": entity_type, "company_id": "1"},
            )
            item["upload_status"] = upload.status_code
            item["upload_body"] = upload.json() if upload.headers.get("content-type", "").startswith("application/json") else {}
            if upload.status_code != 200:
                item["result"] = "FAIL"
                item["notes"].append("upload failed")
                report["results"].append(item)
                continue

            batch = upload.json().get("batch_guid")
            item["batch_guid"] = batch

            validate_staging(batch)
            promote = client.post("/api/v1/etl/promote", data={"batch_guid": batch, "conflict_resolution": "UPDATE"})
            item["promote_status"] = promote.status_code
            item["promote_body"] = promote.json() if promote.headers.get("content-type", "").startswith("application/json") else {"raw": promote.text[:500]}

            with SessionLocal() as db:
                errs = db.query(ETL_ErrorLog).filter(ETL_ErrorLog.batch_guid == batch).all()
                if errs:
                    item["error_count"] = len(errs)
                    item["error_sample"] = [
                        {
                            "type": e.error_type,
                            "table": e.table_name,
                            "message": e.error_message,
                        }
                        for e in errs[:10]
                    ]

            staged_rows = int((item.get("upload_body") or {}).get("staged_rows") or 0)
            error_count = int(item.get("error_count") or 0)
            item["result"] = classify_result(item["promote_status"], item["promote_body"], staged_rows, error_count)

            if item["result"] == "PARTIAL":
                item["notes"].append("partial promotion: mix of success and failure")
            if str(item["result"]).startswith("FAIL") and item["promote_status"] != 200:
                item["notes"].append("promote did not complete")

            created, updated, skipped, failed = summarize_promotion_results(item.get("promote_body") or {})
            item["promote_summary"] = {
                "created": created,
                "updated": updated,
                "skipped": skipped,
                "failed": failed,
            }

            report["results"].append(item)
        except Exception as exc:
            item["result"] = "FAIL"
            item["notes"].append(f"fatal: {exc}")
            report["results"].append(item)

    return report


if __name__ == "__main__":
    out = run()
    out_dir = Path("docs")
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / "finops_pilot_results.json"
    md = out_dir / "implementation" / "FCPL_PILOT_REPORT_FOLDER.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2), encoding="utf-8")
    write_markdown_report(out, md)
    print(json.dumps(out, indent=2))
