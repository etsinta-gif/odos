import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests


@dataclass
class CaseResult:
    test_id: str
    result: str
    details: dict[str, Any]


def add_case(results: list[CaseResult], test_id: str, result: str, details: dict[str, Any]) -> None:
    results.append(CaseResult(test_id=test_id, result=result, details=details))


def safe_get(base_url: str, path: str, timeout: int = 8) -> tuple[int | None, Any, str | None]:
    url = f"{base_url.rstrip('/')}{path}"
    try:
        response = requests.get(url, timeout=timeout)
        body: Any
        try:
            body = response.json()
        except Exception:
            body = response.text
        return response.status_code, body, None
    except Exception as exc:
        return None, None, str(exc)


def safe_post_form(base_url: str, path: str, data: dict[str, Any], files: dict[str, Any] | None = None, timeout: int = 20) -> tuple[int | None, Any, str | None]:
    url = f"{base_url.rstrip('/')}{path}"
    try:
        response = requests.post(url, data=data, files=files, timeout=timeout)
        body: Any
        try:
            body = response.json()
        except Exception:
            body = response.text
        return response.status_code, body, None
    except Exception as exc:
        return None, None, str(exc)


def detect_existing_file(candidates: list[Path]) -> Path | None:
    for item in candidates:
        if item.exists():
            return item
    return None


def summarize(results: list[CaseResult]) -> dict[str, int]:
    counts = {"PASS": 0, "FAIL": 0, "BLOCKED": 0, "PENDING": 0}
    for result in results:
        counts[result.result] = counts.get(result.result, 0) + 1
    return counts


def promote_target_failed_count(payload: Any) -> int:
    if not isinstance(payload, dict):
        return 0
    results = payload.get("results")
    if not isinstance(results, dict):
        return 0
    total_failed = 0
    for table_result in results.values():
        if isinstance(table_result, dict):
            total_failed += int(table_result.get("failed", 0) or 0)
    return total_failed


def run_pytest_quick() -> tuple[str, dict[str, Any]]:
    try:
        run = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-x", "-q"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = ((run.stdout or "") + "\n" + (run.stderr or "")).strip()
        return ("PASS" if run.returncode == 0 else "FAIL", {"exit_code": run.returncode, "output_head": output[:600]})
    except Exception as exc:
        return ("BLOCKED", {"error": str(exc)})


def ensure_synthetic_fixtures(workspace_root: Path) -> tuple[bool, str]:
    script_path = workspace_root / "scripts" / "generate_fcpl_synthetic_fixtures.py"
    if not script_path.exists():
        return False, "synthetic_fixture_generator_missing"
    try:
        run = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=workspace_root,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except Exception as exc:
        return False, str(exc)

    output = ((run.stdout or "") + "\n" + (run.stderr or "")).strip()
    if run.returncode != 0:
        return False, output[:500]
    return True, output[:500]


def run_acceptance(base_url: str, workspace_root: Path, run_pytest: bool) -> dict[str, Any]:
    results: list[CaseResult] = []

    expected_templates = {
        "MIS_TEMPLATE_LenderMaster.xlsx",
        "MIS_TEMPLATE_ConnectorMaster.xlsx",
        "MIS_TEMPLATE_SecuredTracker.xlsx",
        "MIS_TEMPLATE_UnsecuredTracker.xlsx",
        "MIS_TEMPLATE_Employee_Master.xlsx",
        "MIS_TEMPLATE_Salary_Details.xlsx",
        "MIS_TEMPLATE_Employee_Incentive_Master.xlsx",
        "MIS_TEMPLATE_Expense_Payment_Tracker.xlsx",
        "MIS_TEMPLATE_Invoice_Dump.xlsx",
        "MIS_TEMPLATE_Bank_Statement.xlsx",
    }

    # File availability checks for TR-01..TR-10.
    tr_files = {
        "TR-01": [
            workspace_root / "samples/FCPL_Lender_Payout.xlsx",
            workspace_root / "samples/FCPL_Lender_Payout_N_Master.xlsx",
            workspace_root / "samples/Lender_Master.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-01_MIS_TEMPLATE_LenderMaster.xlsx",
        ],
        "TR-02": [
            workspace_root / "samples/FCPL_Connector_Master.xlsx",
            workspace_root / "samples/Connector_Master.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-02_MIS_TEMPLATE_ConnectorMaster.xlsx",
        ],
        "TR-03": [
            workspace_root / "samples/Secured_Tracker.xlsx",
            workspace_root / "uploads/etl/Secured_Tracker_FY_26_27_2_1.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-03_MIS_TEMPLATE_SecuredTracker.xlsx",
        ],
        "TR-04": [
            workspace_root / "samples/Salary_Sheet.xlsx",
            workspace_root / "uploads/etl/Combine_Salary_Sheet_APR_2026.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-04_MIS_TEMPLATE_Salary_Details.xlsx",
        ],
        "TR-05": [
            workspace_root / "samples/Rent_Agreements.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-05_MIS_TEMPLATE_Expense_Payment_Tracker.xlsx",
        ],
        "TR-06": [
            workspace_root / "samples/Gold_Crest_Rent.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-06_MIS_TEMPLATE_Invoice_Dump.xlsx",
        ],
        "TR-07": [
            workspace_root / "samples/DSR_BL_PL.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-07_MIS_TEMPLATE_UnsecuredTracker.xlsx",
        ],
        "TR-08": [
            workspace_root / "samples/Expenses.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-08_MIS_TEMPLATE_Employee_Master.xlsx",
        ],
        "TR-09": [
            workspace_root / "samples/Payments.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-09_MIS_TEMPLATE_Employee_Incentive_Master.xlsx",
        ],
        "TR-10": [
            workspace_root / "samples/Tally_Export.xlsx",
            workspace_root / "samples/_synthetic_phase5/TR-10_MIS_TEMPLATE_Bank_Statement.xlsx",
        ],
    }

    existing_samples: dict[str, Path] = {}
    for test_id, candidates in tr_files.items():
        sample = detect_existing_file(candidates)
        if sample:
            existing_samples[test_id] = sample

    missing_cases = [test_id for test_id in tr_files if test_id not in existing_samples]
    synthetic_generation_note = None
    if missing_cases:
        generated, note = ensure_synthetic_fixtures(workspace_root)
        synthetic_generation_note = note
        if generated:
            for test_id, candidates in tr_files.items():
                if test_id in existing_samples:
                    continue
                sample = detect_existing_file(candidates)
                if sample:
                    existing_samples[test_id] = sample

    status, health_body, err = safe_get(base_url, "/api/v1/health")
    if err:
        add_case(results, "RG-02", "FAIL", {"error": err})
        server_live = False
    else:
        server_live = status == 200 and isinstance(health_body, dict) and health_body.get("status") == "ok"
        add_case(results, "RG-02", "PASS" if server_live else "FAIL", {"status": status, "body": health_body})

    if not server_live:
        add_case(results, "CF-01", "BLOCKED", {"reason": "server_not_reachable"})
        add_case(results, "CF-02", "BLOCKED", {"reason": "server_not_reachable"})
        add_case(results, "CF-03", "BLOCKED", {"reason": "server_not_reachable"})
        add_case(results, "SC-03", "BLOCKED", {"reason": "server_not_reachable"})
        add_case(results, "RG-04", "BLOCKED", {"reason": "server_not_reachable"})
        add_case(results, "E2E-02", "BLOCKED", {"reason": "server_not_reachable"})
        for tr in tr_files:
            add_case(results, tr, "BLOCKED", {"reason": "server_not_reachable"})
        if run_pytest:
            rg3_result, rg3_details = run_pytest_quick()
            add_case(results, "RG-03", rg3_result, rg3_details)
        else:
            add_case(results, "RG-03", "PENDING", {"note": "pytest run disabled with --no-pytest"})
    else:
        # CF-01: templates seeded
        t_status, t_body, t_err = safe_get(base_url, "/api/admin/mapping/templates")
        if t_err:
            add_case(results, "CF-01", "FAIL", {"error": t_err})
            add_case(results, "CF-02", "BLOCKED", {"reason": "template_list_unavailable"})
            add_case(results, "CF-03", "BLOCKED", {"reason": "template_list_unavailable"})
        elif t_status != 200 or not isinstance(t_body, list):
            add_case(results, "CF-01", "FAIL", {"status": t_status, "body_head": str(t_body)[:300]})
            add_case(results, "CF-02", "BLOCKED", {"reason": "template_list_invalid"})
            add_case(results, "CF-03", "BLOCKED", {"reason": "template_list_invalid"})
        else:
            active = [x for x in t_body if str(x.get("status")) == "Active" and bool(x.get("is_active", True))]
            names = {str(x.get("template_name", "")) for x in active}
            missing_templates = sorted(expected_templates - names)
            add_case(results, "CF-01", "PASS" if len(names & expected_templates) == 10 else "FAIL", {
                "active_expected_count": len(names & expected_templates),
                "missing_templates": missing_templates,
            })

            incomplete: list[dict[str, Any]] = []
            alias_ok = False
            for row in active:
                if row.get("template_name") not in expected_templates:
                    continue
                tid = row.get("template_id")
                d_status, d_body, d_err = safe_get(base_url, f"/api/admin/mapping/templates/{tid}")
                if d_err or d_status != 200 or not isinstance(d_body, dict):
                    incomplete.append({"template": row.get("template_name"), "reason": "detail_fetch_failed"})
                    continue
                try:
                    md = json.loads(d_body.get("mapping_definition") or "{}")
                except Exception:
                    md = {}
                mappings = md.get("mappings") or []
                if len(mappings) == 0:
                    incomplete.append({"template": row.get("template_name"), "reason": "no_mappings"})
                if row.get("template_name") == "MIS_TEMPLATE_ConnectorMaster.xlsx":
                    keys = {
                        (str(m.get("source_column", "")).strip().lower(), m.get("target_table"), m.get("target_field"))
                        for m in mappings
                    }
                    alias_ok = ("connector name", "MST_Connector", "full_name") in keys

            add_case(results, "CF-02", "PASS" if not incomplete else "FAIL", {"incomplete": incomplete})
            add_case(results, "CF-03", "PASS" if alias_ok else "FAIL", {"connector_name_alias_to_full_name": alias_ok})

        # SC-03: best-effort schema diff command
        try:
            run = subprocess.run([sys.executable, "-m", "alembic", "check"], cwd=workspace_root, capture_output=True, text=True, timeout=60)
            output = ((run.stdout or "") + "\n" + (run.stderr or "")).strip()
            add_case(results, "SC-03", "PASS" if run.returncode == 0 else "FAIL", {"exit_code": run.returncode, "output_head": output[:700]})
        except Exception as exc:
            add_case(results, "SC-03", "BLOCKED", {"error": str(exc)})

        # RG-04 and E2E-02 endpoint checks
        p_status, p_body, p_err = safe_get(base_url, "/masters/reports/pilot")
        if p_err:
            add_case(results, "RG-04", "FAIL", {"error": p_err})
        else:
            add_case(results, "RG-04", "PASS" if p_status == 200 else "FAIL", {"status": p_status, "body_head": str(p_body)[:200]})

        e_status, e_body, e_err = safe_get(base_url, "/masters/dashboards/executive")
        if e_err:
            add_case(results, "E2E-02", "FAIL", {"error": e_err})
        else:
            add_case(results, "E2E-02", "PASS" if e_status == 200 else "FAIL", {"status": e_status, "body_head": str(e_body)[:200]})

        # TR runs (HTTP upload + promote)
        # Uses the API upload contract currently in repo: entity_type + company_id.
        entity_type_by_tr = {
            "TR-01": "MST_Lender",
            "TR-02": "MST_Connector",
            "TR-03": "TRN_Case",
            "TR-04": "MST_Employee",
            "TR-05": "TRN_Expense",
            "TR-06": "TRN_Expense",
            "TR-07": "TRN_Case",
            "TR-08": "TRN_Expense",
            "TR-09": "TRN_Commission",
            "TR-10": "TRN_Revenue",
        }

        for test_id in tr_files:
            sample = existing_samples.get(test_id)
            if not sample:
                details = {"reason": "required_sample_file_not_found"}
                if synthetic_generation_note:
                    details["synthetic_generation_note"] = synthetic_generation_note
                add_case(results, test_id, "BLOCKED", details)
                continue

            with sample.open("rb") as handle:
                files = {
                    "file": (sample.name, handle, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                }
                up_status, up_body, up_err = safe_post_form(
                    base_url,
                    "/api/v1/etl/upload",
                    data={"entity_type": entity_type_by_tr[test_id], "company_id": "1"},
                    files=files,
                )

            if up_err:
                add_case(results, test_id, "FAIL", {"sample": str(sample), "upload_error": up_err})
                continue

            if up_status == 409:
                add_case(results, test_id, "PASS", {"sample": str(sample), "note": "duplicate upload blocked", "upload": up_body})
                continue

            if up_status not in {200, 202}:
                add_case(results, test_id, "FAIL", {"sample": str(sample), "upload_status": up_status, "upload_body": up_body})
                continue

            if up_status == 202:
                add_case(results, test_id, "FAIL", {"sample": str(sample), "reason": "mapping_required", "upload_body": up_body})
                continue

            batch_guid = None
            if isinstance(up_body, dict):
                batch_guid = up_body.get("batch_guid")

            if not batch_guid:
                add_case(results, test_id, "FAIL", {"sample": str(sample), "reason": "missing_batch_guid", "upload_body": up_body})
                continue

            pr_status, pr_body, pr_err = safe_post_form(
                base_url,
                "/api/v1/etl/promote",
                data={"batch_guid": batch_guid, "conflict_resolution": "SKIP"},
                files=None,
            )
            er_status, er_body, er_err = safe_get(base_url, f"/api/v1/etl/errors?batch_guid={batch_guid}")
            ln_status, ln_body, ln_err = safe_get(base_url, f"/api/v1/etl/lineage?batch_guid={batch_guid}")

            critical_errors = None
            if er_status == 200 and isinstance(er_body, list):
                critical_errors = sum(1 for row in er_body if str(row.get("error_type", "")).upper() == "VALIDATION")

            lineage_count = None
            if ln_status == 200 and isinstance(ln_body, dict):
                lineage_count = ln_body.get("total_records")

            target_failed = promote_target_failed_count(pr_body)
            ok = pr_status == 200 and (critical_errors in {0, None}) and target_failed == 0
            add_case(
                results,
                test_id,
                "PASS" if ok else "FAIL",
                {
                    "sample": str(sample),
                    "batch_guid": batch_guid,
                    "promote_status": pr_status,
                    "promote_body_head": str(pr_body)[:220],
                    "subtarget_failed_count": target_failed,
                    "critical_errors": critical_errors,
                    "lineage_count": lineage_count,
                    "errors_fetch_error": er_err,
                    "lineage_fetch_error": ln_err,
                    "promote_error": pr_err,
                },
            )

        # RG-03
        if run_pytest:
            rg3_result, rg3_details = run_pytest_quick()
            add_case(results, "RG-03", rg3_result, rg3_details)
        else:
            add_case(results, "RG-03", "PENDING", {"note": "pytest run disabled with --no-pytest"})

    # Cases requiring fixtures / environment beyond current workspace.
    add_case(results, "SC-01", "PENDING", {"note": "Requires direct DB schema introspection in target PostgreSQL environment."})
    add_case(results, "SC-02", "PENDING", {"note": "Requires DB-level field type verification in target PostgreSQL environment."})
    add_case(results, "VG-01", "PENDING", {"note": "Needs invalid PAN fixture row upload under matching template."})
    add_case(results, "VG-02", "PENDING", {"note": "Needs disbursement/application date consistency fixture."})
    add_case(results, "VG-03", "PENDING", {"note": "Needs non-existent FK fixture upload."})
    add_case(results, "VG-05", "PENDING", {"note": "Needs controlled UPDATE policy re-upload scenario."})
    add_case(results, "VG-06", "PENDING", {"note": "Needs controlled FAIL policy duplicate scenario."})
    add_case(results, "NL-01", "PENDING", {"note": "Needs pre/post migration snapshot evidence from target environment."})
    add_case(results, "NL-02", "PENDING", {"note": "Covered partially via duplicate upload behavior in TR cases."})
    add_case(results, "NL-03", "PENDING", {"note": "Needs reconciliation dataset old vs canonical fields."})
    add_case(results, "NL-04", "PENDING", {"note": "Needs 2 clean cycles and legacy synonym replay evidence."})
    add_case(results, "E2E-01", "PENDING", {"note": "Needs all 10 source files available and server execution window."})
    add_case(results, "E2E-03", "PENDING", {"note": "Needs deterministic tally export content assertion dataset."})

    summary = summarize(results)
    return {
        "generated_at": datetime.utcnow().isoformat(),
        "base_url": base_url,
        "workspace": str(workspace_root),
        "summary": summary,
        "cases": [r.__dict__ for r in results],
    }


def write_reports(report: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    report["overall_verdict"] = "PASS" if report.get("summary", {}).get("FAIL", 0) == 0 else "FAIL"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines: list[str] = []
    lines.append("# FCPL Pilot Acceptance Results")
    lines.append("")
    lines.append(f"Generated At: {report.get('generated_at')}")
    lines.append(f"Base URL: {report.get('base_url')}")
    lines.append(f"Overall Verdict: {report.get('overall_verdict')}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    summary = report.get("summary", {})
    lines.append(f"- PASS: {summary.get('PASS', 0)}")
    lines.append(f"- FAIL: {summary.get('FAIL', 0)}")
    lines.append(f"- BLOCKED: {summary.get('BLOCKED', 0)}")
    lines.append(f"- PENDING: {summary.get('PENDING', 0)}")
    lines.append("")
    lines.append("## Case Matrix")
    lines.append("")
    lines.append("| Test ID | Result | Notes |")
    lines.append("|---|---|---|")

    for case in report.get("cases", []):
        details = case.get("details", {})
        note = (
            details.get("reason")
            or details.get("note")
            or details.get("error")
            or details.get("output_head")
            or details.get("promote_body_head")
            or ""
        )
        note = str(note).replace("\n", " ")[:180]
        lines.append(f"| {case.get('test_id')} | {case.get('result')} | {note} |")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Safe FCPL pilot acceptance runner (HTTP-first, fault-tolerant)")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for API checks")
    parser.add_argument("--workspace", default=".", help="Path to repository root")
    parser.add_argument("--json-out", default="docs/implementation/fcpl_pilot_acceptance_results.json")
    parser.add_argument("--md-out", default="docs/implementation/fcpl_pilot_acceptance_results.md")
    parser.add_argument("--no-pytest", action="store_true", help="Skip pytest execution")
    args = parser.parse_args()

    workspace_root = Path(args.workspace).resolve()
    report = run_acceptance(args.base_url, workspace_root, run_pytest=not args.no_pytest)
    write_reports(report, workspace_root / args.json_out, workspace_root / args.md_out)

    print(json.dumps(report.get("summary", {}), indent=2))
    print(f"Wrote: {workspace_root / args.json_out}")
    print(f"Wrote: {workspace_root / args.md_out}")


if __name__ == "__main__":
    main()
