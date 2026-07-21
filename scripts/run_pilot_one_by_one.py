import json
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from scripts.validate_staging import validate_staging


def run_pilot() -> dict:
    client = TestClient(app)
    base = Path("samples")

    pilot = [
        ("Lender_Master.xlsx", "MST_Lender", "Master"),
        ("Connector_Master.xlsx", "MST_Connector", "Master"),
        ("Secured_Tracker.xlsx", "TRN_Case", "Master"),
        ("Empty_File.xlsx", "MST_Connector", "Sheet1"),
    ]

    report: dict = {
        "health": {
            "status_code": None,
            "body": None,
        },
        "results": [],
    }

    health = client.get("/api/v1/health")
    report["health"] = {
        "status_code": health.status_code,
        "body": health.json() if health.status_code == 200 else {},
    }

    for fname, entity_type, sheet in pilot:
        item = {
            "file": f"samples/{fname}",
            "entity_type": entity_type,
            "sheet": sheet,
            "result": "UNKNOWN",
            "mapped_columns": 0,
            "ignored_columns": 0,
            "notes": [],
        }

        file_path = base / fname
        if not file_path.exists():
            item["result"] = "FAIL"
            item["notes"].append("file not found")
            report["results"].append(item)
            continue

        data = file_path.read_bytes()

        analyze = client.post(
            "/api/admin/mapping/analyze",
            files={"file": (fname, data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"sheet_name": sheet, "header_row": "1"},
        )
        item["analyze_status"] = analyze.status_code

        if analyze.status_code != 200:
            item["result"] = "FAIL"
            item["notes"].append(f"analyze failed: {analyze.text[:200]}")
            report["results"].append(item)
            continue

        analysis_json = analyze.json()
        sheets = analysis_json.get("sheets") or []
        if not sheets:
            item["result"] = "FAIL"
            item["notes"].append("no sheets in analyze response")
            report["results"].append(item)
            continue

        columns = sheets[0].get("columns", [])
        mappings = []
        for c in columns:
            tgt_t = c.get("suggested_target_table")
            tgt_f = c.get("suggested_target_field")
            if c.get("ignore") or not tgt_t or not tgt_f:
                item["ignored_columns"] += 1
                continue

            source_column = str(c.get("source_column", "")).strip().lower()
            mappings.append(
                {
                    "source_column": c.get("source_column"),
                    "target_table": tgt_t,
                    "target_field": tgt_f,
                    "confidence_score": int(c.get("confidence_score") or 0),
                    "is_verified": True,
                    "is_natural_key": source_column
                    in {"pan", "lender_code", "connector_code", "registration_id", "case_number"},
                    "notes": c.get("notes"),
                }
            )

        item["mapped_columns"] = len(mappings)

        if not mappings:
            item["result"] = "PASS_IGNORE"
            item["notes"].append("no relevant mapping candidates; ignored")
            report["results"].append(item)
            continue

        analyze_full = client.post(
            "/api/admin/mapping/analyze",
            files={"file": (fname, data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"header_row": "1"},
        )
        workbook_fp = analyze_full.json().get("workbook_fingerprint") if analyze_full.status_code == 200 else None

        template_payload = {
            "template_name": f"Pilot {fname.rsplit('.', 1)[0]}",
            "file_pattern": f".*{fname}.*",
            "fingerprint": workbook_fp,
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

        template_id = confirm.json().get("template_id")
        item["template_id"] = template_id

        approve = client.put(f"/api/admin/mapping/templates/{template_id}", json={"status": "Approved"})
        activate = client.put(f"/api/admin/mapping/templates/{template_id}", json={"status": "Active"})
        item["template_approve_status"] = approve.status_code
        item["template_activate_status"] = activate.status_code

        upload1 = client.post(
            "/api/v1/etl/upload",
            files={"file": (fname, data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"entity_type": entity_type, "company_id": "1"},
        )
        item["upload1_status"] = upload1.status_code
        item["upload1_body"] = upload1.json() if upload1.headers.get("content-type", "").startswith("application/json") else {}

        if upload1.status_code != 200:
            item["result"] = "FAIL"
            item["notes"].append("upload1 failed")
            report["results"].append(item)
            continue

        batch1 = upload1.json().get("batch_guid")
        validate_staging(batch1)

        promote1 = client.post("/api/v1/etl/promote", data={"batch_guid": batch1, "conflict_resolution": "UPDATE"})
        lineage1 = client.get("/api/v1/etl/lineage", params={"batch_guid": batch1})
        item["promote1_status"] = promote1.status_code
        item["promote1_body"] = promote1.json() if promote1.headers.get("content-type", "").startswith("application/json") else {}
        item["lineage1_total"] = lineage1.json().get("total_records") if lineage1.status_code == 200 else None

        upload2 = client.post(
            "/api/v1/etl/upload",
            files={"file": (fname, data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            data={"entity_type": entity_type, "company_id": "1"},
        )
        item["upload2_status"] = upload2.status_code
        item["upload2_body"] = upload2.json() if upload2.headers.get("content-type", "").startswith("application/json") else {}

        if upload2.status_code == 200:
            batch2 = upload2.json().get("batch_guid")
            validate_staging(batch2)
            promote2 = client.post("/api/v1/etl/promote", data={"batch_guid": batch2, "conflict_resolution": "UPDATE"})
            lineage2 = client.get("/api/v1/etl/lineage", params={"batch_guid": batch2})
            item["promote2_status"] = promote2.status_code
            item["promote2_body"] = promote2.json() if promote2.headers.get("content-type", "").startswith("application/json") else {}
            item["lineage2_total"] = lineage2.json().get("total_records") if lineage2.status_code == 200 else None

        if item.get("promote1_status") == 200:
            item["result"] = "PASS"
        elif item.get("upload1_status") == 200:
            item["result"] = "PARTIAL"
            item["notes"].append("upload succeeded but promote did not complete")
        else:
            item["result"] = "FAIL"

        report["results"].append(item)

    return report


if __name__ == "__main__":
    try:
        output = run_pilot()
    except Exception as exc:
        output = {"fatal_error": str(exc)}
    out_path = Path("docs")
    out_path.mkdir(parents=True, exist_ok=True)
    final_path = out_path / "pilot_run_results_final.json"
    final_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))
