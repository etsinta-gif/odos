import io

from openpyxl import Workbook
import pandas as pd

from src.admin.services.file_analyzer import detect_slab_columns, infer_column_type
from src.admin.services.mapper import apply_mapping, generate_mapping_proposal


def test_infer_column_type_text() -> None:
    series = pd.Series(["apple", "banana", "cherry"])
    result = infer_column_type(series)
    assert result["type"] == "text"
    assert result["null_count"] == 0
    assert result["unique_count"] == 3


def test_infer_column_type_amount() -> None:
    series = pd.Series([1, 2, 3])
    result = infer_column_type(series)
    assert result["type"] == "amount"


def test_infer_column_type_percentage() -> None:
    series = pd.Series([0.1, 0.2, 0.3])
    result = infer_column_type(series)
    assert result["type"] == "percentage"


def test_detect_slab_columns() -> None:
    columns = ["Amount", "< ₹50 L", "₹50 L - < ₹1 Cr", "Rate"]
    slabs = detect_slab_columns(columns)
    assert "< ₹50 L" in slabs
    assert slabs["< ₹50 L"]["transformation"] == "UNPIVOT"
    assert slabs["< ₹50 L"]["tier_min"] == 0.0
    assert slabs["< ₹50 L"]["tier_max"] == 5000000.0


def test_generate_mapping_proposal() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "lender_name", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "pan", "inferred_type": "text", "pattern": "pan", "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "unknown_column", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }
    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]
    assert cols[0]["suggested_target_table"] == "MST_Lender"
    assert cols[1]["suggested_target_field"] == "pan"
    assert cols[2]["ignore"] is True


def test_generate_mapping_proposal_alias_for_lender_nbfc() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Lender / NBFC", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }
    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]
    assert col["suggested_target_table"] == "MST_Lender"
    assert col["suggested_target_field"] == "lender_name"
    assert col["confidence_score"] >= 90
    assert col["confidence_level"] == "High"


def test_generate_mapping_proposal_alias_for_nbfc_flag() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "NBFC?", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }
    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]
    assert col["suggested_target_table"] == "MST_Lender"
    assert col["suggested_target_field"] == "is_nbfc"
    assert col["confidence_score"] >= 90


def test_generate_mapping_proposal_contextual_bank_name_for_connector_sheet() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Connector Master",
                "columns": [
                    {"source_column": "Bank Name", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]

    assert col["suggested_target_table"] == "MST_Connector"
    assert col["suggested_target_field"] == "bank_name"
    assert col["lookup"]["table"] == "MST_Connector"
    assert col["lookup"]["field"] == "bank_name"


def test_generate_mapping_proposal_pattern_for_gstin() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Tax Number", "inferred_type": "text", "pattern": "gstin", "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }
    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]
    assert col["suggested_target_table"] == "MST_Lender"
    assert col["suggested_target_field"] == "gstin"


def test_generate_mapping_proposal_for_commission_rule_fields() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Rules",
                "columns": [
                    {"source_column": "Base %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Headline %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "PF %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "I %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Slab Type", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Qualifying Notes", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Commercial", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Post-disbursement clawback conditions", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "RUL_CommissionRule"
    assert cols[0]["suggested_target_field"] == "base_percent"
    assert cols[1]["suggested_target_field"] == "headline_percent"
    assert cols[2]["suggested_target_field"] == "pf_percent"
    assert cols[3]["suggested_target_field"] == "i_percent"
    assert cols[4]["suggested_target_field"] == "slab_type"
    assert cols[5]["suggested_target_field"] == "qualifying_notes"
    assert cols[6]["suggested_target_field"] == "commercial_terms"
    assert cols[7]["suggested_target_field"] == "clawback_conditions"


def test_generate_mapping_proposal_for_dsa_and_product_roi() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "DSA", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "ROI %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "MST_DSA"
    assert cols[0]["suggested_target_field"] == "dsa_code"
    assert cols[1]["suggested_target_table"] == "MST_Product"
    assert cols[1]["suggested_target_field"] == "roi_percent"


def test_generate_mapping_proposal_for_product_attributes() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Salary Range", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Employer", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "MST_Product"
    assert cols[0]["suggested_target_field"] == "borrower_salary_range"
    assert cols[1]["suggested_target_table"] == "MST_Product"
    assert cols[1]["suggested_target_field"] == "is_employed"


def test_generate_mapping_proposal_for_reference_dimension_columns() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Type", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Channel", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Borrower", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Nature", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Location", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "REF_LoanType"
    assert cols[0]["suggested_target_field"] == "name"
    assert cols[1]["suggested_target_table"] == "REF_Channel"
    assert cols[1]["suggested_target_field"] == "name"
    assert cols[2]["suggested_target_table"] == "REF_BorrowerProfile"
    assert cols[2]["suggested_target_field"] == "name"
    assert cols[3]["suggested_target_table"] == "REF_LoanNature"
    assert cols[3]["suggested_target_field"] == "name"
    assert cols[4]["suggested_target_table"] == "REF_Location"
    assert cols[4]["suggested_target_field"] == "name"


def test_generate_mapping_proposal_ignores_serial_number_column() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Sr. No.", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]

    assert col["ignore"] is True
    assert col["confidence_score"] == 0
    assert col["notes"] == "Serial number column"


def test_generate_mapping_proposal_for_bl_pl_lender_master_context() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "BL",
                "columns": [
                    {"source_column": "COMPANY NAME", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "PRODUCT", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "BANK NAME", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "MST_Lender"
    assert cols[0]["suggested_target_field"] == "lender_name"
    assert cols[1]["suggested_target_table"] == "MST_Product"
    assert cols[1]["suggested_target_field"] == "product_name"
    assert cols[2]["suggested_target_table"] == "MST_Lender"
    assert cols[2]["suggested_target_field"] == "lender_name"


def test_generate_mapping_proposal_marks_pre_disbursement_scope_for_bl_pl() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "BL",
                "columns": [
                    {"source_column": "SANCTION AMT", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "LOGIN DATE", "inferred_type": "date", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    sheet = result["sheets"][0]

    assert sheet["business_scope"] == "PRE_DISBURSEMENT_MIS"
    assert sheet["business_domain"] == ["lender", "product"]
    assert sheet["descoped_from"] == ["operations"]
    assert sheet["columns"][0]["ignore"] is True
    assert sheet["columns"][1]["ignore"] is True
    assert "descoped operations column" in sheet["columns"][0]["notes"]


def test_generate_mapping_proposal_for_tracker_payout_lifecycle() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Tracker",
                "columns": [
                    {"source_column": "PAYMENT AMT", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "TDS@2%", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Payment Request Date C-1", "inferred_type": "date", "pattern": "date", "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "BANK PAYOUT%", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "UNIT HEAD", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "UNIT HEAD%", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "TRN_Payment"
    assert cols[0]["suggested_target_field"] == "payment_amount"
    assert cols[1]["suggested_target_table"] == "TRN_Commission"
    assert cols[1]["suggested_target_field"] == "tds_amount"
    assert cols[2]["suggested_target_table"] == "TRN_Payment"
    assert cols[2]["suggested_target_field"] == "payment_date"
    assert cols[3]["suggested_target_table"] == "RUL_CommissionRule"
    assert cols[3]["suggested_target_field"] == "headline_percent"
    assert cols[4]["suggested_target_table"] == "MST_Employee"
    assert cols[4]["suggested_target_field"] == "full_name"
    assert cols[5]["suggested_target_table"] == "RUL_CommissionRule"
    assert cols[5]["suggested_target_field"] == "headline_percent"


def test_generate_mapping_proposal_for_tracker_branch_referral_and_unnamed() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Tracker",
                "columns": [
                    {"source_column": "CODE", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "BRANCH", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Referred by", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Unnamed: 44", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    cols = result["sheets"][0]["columns"]

    assert cols[0]["suggested_target_table"] == "MST_DSA"
    assert cols[0]["suggested_target_field"] == "dsa_code"
    assert cols[1]["suggested_target_table"] == "TRN_Case"
    assert cols[1]["suggested_target_field"] == "branch_name"
    assert cols[2]["suggested_target_table"] == "TRN_Case"
    assert cols[2]["suggested_target_field"] == "referral_source"
    assert cols[3]["ignore"] is True
    assert cols[3]["notes"] == "Unnamed helper column"


def test_generate_mapping_proposal_for_salary_sheet_context() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Payroll Sheet",
                "columns": [
                    {"source_column": "ID", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Employee Name", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "PAN", "inferred_type": "text", "pattern": "pan", "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Bank Name", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Bank Account Number", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Designation", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Net Payable", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Salary Paid Status", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "UTR NUMBER", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Days Worked", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "Other Allowance / Incentives", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "P.TAX", "inferred_type": "amount", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "FCPL DOJ", "inferred_type": "date", "pattern": "date", "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                    {"source_column": "PF Remark", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    sheet = result["sheets"][0]
    cols = sheet["columns"]

    assert sheet["business_scope"] == "EMPLOYEE_SALARY"
    assert cols[0]["suggested_target_table"] == "MST_Employee"
    assert cols[0]["suggested_target_field"] == "employee_code"
    assert cols[1]["suggested_target_field"] == "full_name"
    assert cols[2]["suggested_target_field"] == "pan"
    assert cols[3]["suggested_target_field"] == "bank_name"
    assert cols[4]["suggested_target_field"] == "bank_account_number"
    assert cols[5]["suggested_target_field"] == "designation"
    assert cols[6]["suggested_target_table"] == "TRN_Payment"
    assert cols[6]["suggested_target_field"] == "payment_amount"
    assert cols[7]["suggested_target_field"] == "reconciliation_status"
    assert cols[8]["suggested_target_field"] == "utr_number"
    assert cols[9]["suggested_target_table"] == "TRN_Payment"
    assert cols[9]["suggested_target_field"] == "notes"
    assert cols[10]["suggested_target_table"] == "TRN_Commission"
    assert cols[10]["suggested_target_field"] == "bonus_commission_amount"
    assert cols[11]["suggested_target_table"] == "TRN_Expense"
    assert cols[11]["suggested_target_field"] == "amount"
    assert cols[12]["suggested_target_table"] == "MST_Employee"
    assert cols[12]["suggested_target_field"] == "date_of_joining"
    assert cols[13]["suggested_target_table"] == "TRN_Payment"
    assert cols[13]["suggested_target_field"] == "notes"


def test_generate_mapping_proposal_for_salary_pivot_sheet() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Pivot",
                "columns": [
                    {"source_column": "Unnamed: 0", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    sheet = result["sheets"][0]
    col = sheet["columns"][0]

    assert sheet["business_scope"] == "EMPLOYEE_SALARY_SUMMARY"
    assert col["ignore"] is True
    assert col["notes"] == "Salary pivot summary column"


def test_analyze_excel_bytes_detects_formulas() -> None:
    from src.admin.services.file_analyzer import analyze_excel_bytes

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Tracker"
    worksheet.append(["Case Number", "Base %", "Amount"])
    worksheet.append(["CASE-001", "=C2*0.01", 100000])
    worksheet.append(["CASE-002", "=C3*0.02", 150000])

    buffer = io.BytesIO()
    workbook.save(buffer)

    result = analyze_excel_bytes(buffer.getvalue(), sheet_name="Tracker", header_row=1)
    columns = result["sheets"][0]["columns"]
    base_col = next(column for column in columns if column["source_column"] == "Base %")

    assert base_col["formula_detected"] is True
    assert base_col["formula_count"] == 2
    assert base_col["formula_status"] in {"FORMULA_DETECTED", "FORMULA_ERRORS"}
    assert len(base_col["formula_samples"]) >= 1


def test_generate_mapping_proposal_does_not_force_unrelated_percentage_to_slab() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Rules",
                "columns": [
                    {"source_column": "Contest Bonus %", "inferred_type": "percentage", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }

    result = generate_mapping_proposal(sample_analysis)
    col = result["sheets"][0]["columns"][0]

    assert col["suggested_target_table"] == "RUL_Contest"
    assert col["suggested_target_field"] == "bonus_percent"
    assert col["ignore"] is False


def test_generate_mapping_without_proposal_keeps_suggestions_empty() -> None:
    sample_analysis = {
        "sheets": [
            {
                "sheet_name": "Master",
                "columns": [
                    {"source_column": "Lender / NBFC", "inferred_type": "text", "pattern": None, "suggested_target_table": None, "suggested_target_field": None, "confidence_score": 0, "ignore": False, "notes": None},
                ],
            }
        ]
    }
    col = sample_analysis["sheets"][0]["columns"][0]
    assert col["suggested_target_table"] is None
    assert col["suggested_target_field"] is None


def test_apply_mapping_builds_table_field_keys() -> None:
    row = {"PAN": "ABCDE1234F", "Lender / NBFC": "Axis"}
    mapping = {
        "PAN": {"target_table": "MST_Lender", "target_field": "pan"},
        "Lender / NBFC": {"target_table": "MST_Lender", "target_field": "lender_name"},
    }
    result = apply_mapping(row, mapping)
    assert result["MST_Lender.pan"] == "ABCDE1234F"
    assert result["MST_Lender.lender_name"] == "Axis"
