import json
import sys
from datetime import date
from pathlib import Path

from openpyxl import Workbook

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.metadata.services.fixed_template_bootstrap import FIXED_TEMPLATE_SPECS

OUT_DIR = REPO_ROOT / "samples" / "_synthetic_phase5"
MANIFEST_PATH = REPO_ROOT / "docs" / "implementation" / "synthetic_fixture_manifest.json"

CASE_TEMPLATE_MAP = {
    "TR-01": "MIS_TEMPLATE_LenderMaster.xlsx",
    "TR-02": "MIS_TEMPLATE_ConnectorMaster.xlsx",
    "TR-03": "MIS_TEMPLATE_SecuredTracker.xlsx",
    "TR-04": "MIS_TEMPLATE_Salary_Details.xlsx",
    "TR-05": "MIS_TEMPLATE_Expense_Payment_Tracker.xlsx",
    "TR-06": "MIS_TEMPLATE_Invoice_Dump.xlsx",
    "TR-07": "MIS_TEMPLATE_UnsecuredTracker.xlsx",
    "TR-08": "MIS_TEMPLATE_Employee_Master.xlsx",
    "TR-09": "MIS_TEMPLATE_Employee_Incentive_Master.xlsx",
    "TR-10": "MIS_TEMPLATE_Bank_Statement.xlsx",
}


def _sample_value(column_name: str) -> object:
    normalized = column_name.strip().lower()
    if "date" in normalized:
        return date(2026, 4, 1)
    if any(token in normalized for token in ["amount", "gross", "net", "target", "share", "earnings", "salary", "basic", "allowance"]):
        return 100000
    if "%" in column_name or "percent" in normalized or "rate" in normalized:
        return 2.5
    if "pan" in normalized:
        return "ABCDE1234F"
    if "gst" in normalized and "payout" in normalized:
        return 18000
    if "gst" in normalized and "amount" not in normalized:
        return "27ABCDE1234F1Z5"
    if "ifsc" in normalized:
        return "HDFC0001234"
    if "utr" in normalized:
        return "UTR-0001"
    if "code" in normalized:
        return 1001
    if "name" in normalized:
        return "Sample Name"
    if "month" in normalized:
        return "2026-04"
    if any(token in normalized for token in ["is_", "include", "cancelled", "nbfc"]):
        return False
    if "number" in normalized or "account" in normalized:
        return "100200300400"
    return 1


def _columns_for_template(template_name: str) -> tuple[str, int, list[str]]:
    if template_name == "MIS_TEMPLATE_UnsecuredTracker.xlsx":
        template_name = "MIS_TEMPLATE_SecuredTracker.xlsx"
    for spec in FIXED_TEMPLATE_SPECS:
        if spec["template_name"] == template_name:
            columns = [str(m["source_column"]).strip() for m in spec.get("mappings", []) if str(m.get("source_column") or "").strip()]
            deduped = list(dict.fromkeys(columns))
            return spec["sheet_name"], int(spec["header_row"]), deduped
    raise ValueError(f"Unknown template: {template_name}")


def _build_workbook(sheet_name: str, header_row: int, columns: list[str]) -> Workbook:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = sheet_name

    while sheet.max_row < header_row - 1:
        sheet.append([])

    sheet.append(columns)
    sheet.append([_sample_value(col) for col in columns])
    return workbook


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    manifest: dict[str, dict[str, object]] = {}
    for case_id, template_name in CASE_TEMPLATE_MAP.items():
        sheet_name, header_row, columns = _columns_for_template(template_name)
        out_file = OUT_DIR / f"{case_id}_{template_name}"
        workbook = _build_workbook(sheet_name, header_row, columns)
        workbook.save(out_file)

        manifest[case_id] = {
            "template_name": template_name,
            "sheet_name": sheet_name,
            "header_row": header_row,
            "output_file": str(out_file.relative_to(REPO_ROOT)).replace("\\", "/"),
            "column_count": len(columns),
        }

    MANIFEST_PATH.write_text(json.dumps({"generated_cases": manifest}, indent=2), encoding="utf-8")
    print(json.dumps({"generated": len(manifest), "output_dir": str(OUT_DIR), "manifest": str(MANIFEST_PATH)}, indent=2))


if __name__ == "__main__":
    main()
