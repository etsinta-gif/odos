import re
from typing import Any

from src.admin.services.file_analyzer import detect_slab_columns


KNOWN_MAPPINGS = {
    # Lender fields
    "lender_name": {"table": "MST_Lender", "field": "lender_name"},
    "pan": {"table": "MST_Lender", "field": "pan"},
    "gstin": {"table": "MST_Lender", "field": "gstin"},
    "lender_code": {"table": "MST_Lender", "field": "lender_code"},
    "is_nbfc": {"table": "MST_Lender", "field": "is_nbfc"},
    "dsa_code": {"table": "MST_DSA", "field": "dsa_code"},
    "dsa": {"table": "MST_DSA", "field": "dsa_code"},
    # Connector fields
    "connector_code": {"table": "MST_Connector", "field": "connector_code"},
    "connector_name": {"table": "MST_Connector", "field": "full_name"},
    "full_name": {"table": "MST_Connector", "field": "full_name"},
    "bank_name": {"table": "MST_Connector", "field": "bank_name"},
    "account_number": {"table": "MST_Connector", "field": "account_number"},
    "ifsc": {"table": "MST_Connector", "field": "ifsc"},
    "connector_pan": {"table": "MST_Connector", "field": "pan"},
    "connector_bank": {"table": "MST_Connector", "field": "bank_name"},
    "connector_account_no": {"table": "MST_Connector", "field": "account_number"},
    "connector_ifsc_code": {"table": "MST_Connector", "field": "ifsc"},
    "connector_gst": {"table": "MST_Connector", "field": "gstin"},
    # Product fields
    "product_name": {"table": "MST_Product", "field": "product_name"},
    "product_code": {"table": "MST_Product", "field": "product_code"},
    "min_loan_amount": {"table": "MST_Product", "field": "min_loan_amount"},
    "max_loan_amount": {"table": "MST_Product", "field": "max_loan_amount"},
    "interest_rate": {"table": "MST_Product", "field": "interest_rate"},
    "roi_percent": {"table": "MST_Product", "field": "roi_percent"},
    "borrower_salary_range": {"table": "MST_Product", "field": "borrower_salary_range"},
    "is_employed": {"table": "MST_Product", "field": "is_employed"},
    "active": {"table": "MST_Product", "field": "is_active"},
    "category": {"table": "MST_Product", "field": "product_name"},
    "sub_product": {"table": "MST_Product", "field": "sub_product"},
    # Commission rule fields
    "slab_type": {"table": "RUL_CommissionRule", "field": "slab_type"},
    "base_percent": {"table": "RUL_CommissionRule", "field": "base_percent"},
    "headline_percent": {"table": "RUL_CommissionRule", "field": "headline_percent"},
    "pf_percent": {"table": "RUL_CommissionRule", "field": "pf_percent"},
    "i_percent": {"table": "RUL_CommissionRule", "field": "i_percent"},
    "qualifying_condition": {"table": "RUL_CommissionRule", "field": "qualifying_condition"},
    "qualifying_notes": {"table": "RUL_CommissionRule", "field": "qualifying_notes"},
    "commercial_terms": {"table": "RUL_CommissionRule", "field": "commercial_terms"},
    "clawback_conditions": {"table": "RUL_CommissionRule", "field": "clawback_conditions"},
    "contest_frequency": {"table": "RUL_Contest", "field": "frequency"},
    "contest_target": {"table": "RUL_Contest", "field": "target_amount"},
    "contest_bonus_percent": {"table": "RUL_Contest", "field": "bonus_percent"},
    "contest_period": {"table": "RUL_Contest", "field": "period"},
    "contest_notes": {"table": "RUL_Contest", "field": "notes"},
    # Case fields
    "case_number": {"table": "TRN_Case", "field": "case_number"},
    "sanction_amount": {"table": "TRN_Case", "field": "sanction_amount"},
    "disbursement_amount": {"table": "TRN_Case", "field": "disbursement_amount"},
    "status": {"table": "TRN_Case", "field": "status"},
    "customer_id": {"table": "TRN_Case", "field": "customer_id"},
    "lender_id": {"table": "TRN_Case", "field": "lender_id"},
    "product_id": {"table": "TRN_Case", "field": "product_id"},
    "connector_id": {"table": "TRN_Case", "field": "connector_id"},
    "application_date": {"table": "TRN_Case", "field": "application_date"},
    "branch_code": {"table": "TRN_Case", "field": "branch_code"},
    "branch_name": {"table": "TRN_Case", "field": "branch_name"},
    "referral_source": {"table": "TRN_Case", "field": "referral_source"},
}

ALIASES = {
    # Lender aliases
    "lender_nbfc": "lender_name",
    "lender_or_nbfc": "lender_name",
    "lender_nbfc_name": "lender_name",
    "company_name": "lender_name",
    "company": "lender_name",
    "nbfc": "is_nbfc",
    "nbfc_flag": "is_nbfc",
    "is_nbfc": "is_nbfc",
    # Connector aliases
    "customer_name": "full_name",
    "contact_name": "full_name",
    "registration_id": "connector_code",
    "connector_id": "connector_code",
    "connector_pan": "connector_pan",
    "connector_bank": "connector_bank",
    "connector_account_no": "connector_account_no",
    "connector_ifsc_code": "connector_ifsc_code",
    "ifsc_code": "ifsc",
    "account_no": "account_number",
    "bank": "bank_name",
    "bank_1": "bank_name",
    "account_no_1": "account_number",
    "ifsc_code_1": "ifsc",
    "referred_by": "referral_source",
    # Product aliases
    "product_category": "category",
    "product": "product_name",
    "max_tenure_months": "interest_rate",
    "lending_product": "product_name",
    "is_active": "active",
    "subproduct": "sub_product",
    "roi": "roi_percent",
    "salary_range": "borrower_salary_range",
    "borrower_salary_range": "borrower_salary_range",
    "employer": "is_employed",
    "is_employed": "is_employed",
    # Commission rule aliases
    "base": "base_percent",
    "base_pct": "base_percent",
    "headline": "headline_percent",
    "headline_pct": "headline_percent",
    "pf": "pf_percent",
    "pf_pct": "pf_percent",
    "i": "i_percent",
    "insurance": "i_percent",
    "insurance_pct": "i_percent",
    "qualifying": "qualifying_condition",
    "commercial": "commercial_terms",
    "clawback": "clawback_conditions",
    "post_disbursement_clawback_conditions": "clawback_conditions",
    "contest_frequency": "contest_frequency",
    "contest_target": "contest_target",
    "contest_bonus": "contest_bonus_percent",
    "contest_bonus_pct": "contest_bonus_percent",
    "contest_period": "contest_period",
    "contest_notes": "contest_notes",
    "slab": "slab_type",
}

OPERATIONS_DESCOPED_COLUMNS = {
    "sanction_amount",
    "sanction_amt",
    "disbursement_amount",
    "disburse_amt",
    "disb_amt",
    "net_amount",
    "net_amt",
    "login_amount",
    "login_amt",
    "interest_rate",
    "rate",
    "processing_fee",
    "pf",
    "processing_fee_rate",
    "insurance_amount",
    "insurance",
    "tenure_months",
    "tenure",
    "subvention_rate",
    "subvention",
    "login_date",
    "sanction_date",
    "disbursement_date",
    "remarks",
    "remark",
    "status",
}


def _sheet_business_context(sheet_name: str, columns: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    normalized = _normalize_header(sheet_name)
    columns = columns or []
    if "pivot" in normalized:
        return {
            "business_domain": ["employee", "salary", "summary"],
            "business_scope": "EMPLOYEE_SALARY_SUMMARY",
            "descoped_from": ["direct_import"],
            "notes": "Salary pivot summary context; usually review-only and not imported directly.",
        }
    if "salary" in normalized or "payroll" in normalized:
        return {
            "business_domain": ["employee", "salary"],
            "business_scope": "EMPLOYEE_SALARY",
            "descoped_from": [],
            "notes": "Employee salary payroll context.",
        }
    if "bank_account_master" in normalized or ("connector" in normalized and "master" in normalized):
        return {
            "business_domain": ["connector", "master"],
            "business_scope": "CONNECTOR_BANK_MASTER",
            "descoped_from": [],
            "notes": "Connector bank account master context.",
        }
    if "tracker" in normalized:
        return {
            "business_domain": ["transaction", "commission", "secured"],
            "business_scope": "COMMISSION_PAYOUT_TRACKER",
            "descoped_from": [],
            "notes": "Transaction and commission payout tracker context.",
        }
    if "rent" in normalized:
        return {
            "business_domain": ["expense", "rent"],
            "business_scope": "RENT_EXPENSE",
            "descoped_from": [],
            "notes": "Rent expense context.",
        }
    if "expense" in normalized:
        return {
            "business_domain": ["expense", "general"],
            "business_scope": "GENERAL_EXPENSE",
            "descoped_from": [],
            "notes": "General expense context.",
        }
    if normalized in {"bl", "pl"} or any(token in normalized for token in {"mis", "payout", "lender", "loan"}):
        return {
            "business_domain": ["lender", "product"],
            "business_scope": "PRE_DISBURSEMENT_MIS",
            "descoped_from": ["operations"],
            "notes": "Pre-disbursement lender/product MIS; operations-only columns are intentionally descoped.",
        }
    if any(_normalize_header(str(col.get("source_column", ""))) in {"company_name", "product", "bank_name"} for col in columns):
        return {
            "business_domain": ["lender", "product"],
            "business_scope": "MIS",
            "descoped_from": [],
            "notes": "Business MIS context inferred from lender/product columns.",
        }
    return {
        "business_domain": [],
        "business_scope": "GENERIC",
        "descoped_from": [],
        "notes": None,
    }


def _normalize_header(value: str) -> str:
    norm = re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower())
    norm = re.sub(r"_+", "_", norm).strip("_")
    return norm


def _confidence_level(score: int) -> str:
    if score >= 85:
        return "High"
    if score >= 60:
        return "Medium"
    if score > 0:
        return "Low"
    return "None"


def _apply_formula_context(column: dict[str, Any]) -> None:
    formula_detected = bool(column.get("formula_detected"))
    formula_error_count = int(column.get("formula_error_count") or 0)
    if not formula_detected:
        column["confidence_level"] = _confidence_level(int(column.get("confidence_score") or 0))
        return

    if formula_error_count > 0:
        column["confidence_score"] = max(int(column.get("confidence_score") or 0) - 15, 0)
        column.setdefault("notes", "")
        existing_notes = str(column.get("notes") or "").strip()
        formula_note = f"Formula discrepancy detected in source workbook ({formula_error_count} issue(s))"
        column["notes"] = f"{existing_notes}; {formula_note}".strip("; ").strip() if existing_notes else formula_note
    else:
        column["confidence_score"] = min(int(column.get("confidence_score") or 0) + 5, 100)
        column.setdefault("notes", "")
        existing_notes = str(column.get("notes") or "").strip()
        formula_note = "Formula-backed source column validated against workbook"
        column["notes"] = f"{existing_notes}; {formula_note}".strip("; ").strip() if existing_notes else formula_note

    column["confidence_level"] = _confidence_level(int(column.get("confidence_score") or 0))


def _mapping_for_source(source_raw: str, known_mappings: dict[str, Any]) -> tuple[str, str, int, str] | None:
    source = _normalize_header(source_raw)

    direct = known_mappings.get(source)
    if direct:
        return direct["table"], direct["field"], 95, "Exact normalized match"

    alias_key = ALIASES.get(source)
    if alias_key and alias_key in known_mappings:
        mapped = known_mappings[alias_key]
        return mapped["table"], mapped["field"], 92, f"Alias match with '{alias_key}'"

    for key, mapping in known_mappings.items():
        if source == key or source.startswith(f"{key}_") or key in source:
            return mapping["table"], mapping["field"], 75, f"Keyword match with '{key}'"

    return None


def _contextual_mapping_for_source(source_raw: str, sheet_name: str, columns: list[dict[str, Any]]) -> dict[str, Any] | None:
    source = _normalize_header(source_raw)
    source_text = str(source_raw or "").strip().lower()
    sheet = _normalize_header(sheet_name)
    salary_sheet = "salary" in sheet or "payroll" in sheet
    salary_pivot_sheet = "pivot" in sheet
    lender_sheet = any(token in sheet for token in {"bl", "pl", "mis", "payout", "lender", "loan"})
    tracker_sheet = "tracker" in sheet
    connector_master_sheet = "bank_account_master" in sheet or ("connector" in sheet and "master" in sheet)
    connector_sheet = connector_master_sheet or any(token in sheet for token in {"connector", "secured"})

    def _lookup(table: str, field: str, create_if_missing: bool = False) -> dict[str, Any]:
        return {"table": table, "field": field, "create_if_missing": create_if_missing}

    if salary_pivot_sheet:
        return {
            "ignore": True,
            "confidence_score": 0,
            "notes": "Salary pivot summary column",
        }

    if salary_sheet:
        if source.startswith("unnamed"):
            return {
                "ignore": True,
                "confidence_score": 0,
                "notes": "Unnamed helper column",
            }

        salary_employee_field_map = {
            "id": "employee_code",
            "employee_name": "full_name",
            "gender": "gender",
            "dob": "date_of_birth",
            "father_name": "father_name",
            "marrital_status": "marital_status",
            "pan": "pan",
            "aadhar_number": "aadhar_number",
            "address": "address",
            "date_of_joining": "date_of_joining",
            "designation": "designation",
            "department": "department",
            "team_name": "team_name",
            "pf_aplicable": "pf_applicable",
            "esic_aplicable": "esic_applicable",
            "email_id": "email",
            "mobile_no": "mobile",
            "bank_name": "bank_name",
            "bank_account_number": "bank_account_number",
            "bank_ifsc": "bank_ifsc",
            "uan_number": "uan_number",
            "unit_head": "full_name",
            "sm_name": "full_name",
        }
        if source in salary_employee_field_map:
            return {
                "suggested_target_table": "MST_Employee",
                "suggested_target_field": salary_employee_field_map[source],
                "confidence_score": 90,
                "notes": "Salary sheet employee attribute",
                "lookup": _lookup("MST_Employee", salary_employee_field_map[source], True),
            }

        if source in {"fcpl_doj"}:
            return {
                "suggested_target_table": "MST_Employee",
                "suggested_target_field": "date_of_joining",
                "confidence_score": 86,
                "notes": "Salary sheet joining date variant",
                "lookup": _lookup("MST_Employee", "date_of_joining", True),
            }

        if source in {"net_payable", "salary_for_the_month", "salary_paid_status", "utr_number", "remark", "remark_1"}:
            salary_payment_field_map = {
                "net_payable": "payment_amount",
                "salary_for_the_month": "payment_amount",
                "salary_paid_status": "reconciliation_status",
                "utr_number": "utr_number",
                "remark": "notes",
                "remark_1": "notes",
            }
            return {
                "suggested_target_table": "TRN_Payment",
                "suggested_target_field": salary_payment_field_map[source],
                "confidence_score": 84,
                "notes": "Salary sheet payout attribute",
            }

        if source in {"days_worked", "leaves", "payable_days", "total_leaves", "completed_months", "pf_remark"}:
            return {
                "suggested_target_table": "TRN_Payment",
                "suggested_target_field": "notes",
                "confidence_score": 62,
                "notes": "Salary sheet attendance and payroll metadata",
            }

        if source in {"firm"}:
            return {
                "suggested_target_table": "TRN_Case",
                "suggested_target_field": "branch_name",
                "confidence_score": 66,
                "notes": "Salary sheet organizational unit",
            }

        if source in {"other_allowance_incentives"}:
            return {
                "suggested_target_table": "TRN_Commission",
                "suggested_target_field": "bonus_commission_amount",
                "confidence_score": 70,
                "notes": "Salary sheet incentive and commission component",
            }

        if source in {
            "tds",
            "pf",
            "esic",
            "advance_salary",
            "ctc",
            "gross_salary",
            "salary_increase",
            "one_day_salary",
            "basic_da",
            "hra",
            "other_allowance",
            "total_leaves_gross_earning",
            "basic",
            "hra_1",
            "overtime",
            "total_leaves_gross_earning_1",
            "diff",
            "p_tax",
            "mlwf",
            "exp",
            "pf_wages",
            "ee_share",
            "er_share",
            "pension",
            "black1",
            "esic_wages",
            "ee_share_1",
            "er_share_1",
        }:
            return {
                "suggested_target_table": "TRN_Expense",
                "suggested_target_field": "amount",
                "confidence_score": 68,
                "notes": "Salary sheet payroll amount",
            }

    if source in {"sr_no", "s_no", "serial_no", "serial_number", "srnumber", "srno"}:
        return {
            "ignore": True,
            "confidence_score": 0,
            "notes": "Serial number column",
        }

    if source.startswith("unnamed"):
        return {
            "ignore": True,
            "confidence_score": 0,
            "notes": "Unnamed helper column",
        }

    if source in {"bank_name", "lender_name"}:
        if tracker_sheet:
            return {
                "suggested_target_table": "MST_Lender",
                "suggested_target_field": "lender_name",
                "confidence_score": 92,
                "notes": "Tracker context lender lookup",
                "lookup": _lookup("MST_Lender", "lender_name", True),
            }
        if lender_sheet:
            return {
                "suggested_target_table": "MST_Lender",
                "suggested_target_field": "lender_name",
                "confidence_score": 92,
                "notes": "Lender master sheet context",
                "lookup": _lookup("MST_Lender", "lender_name", True),
            }
        if connector_sheet or any(
            _normalize_header(str(col.get("source_column", ""))) in {"connector_code", "connector_name", "full_name"} for col in columns
        ):
            return {
                "suggested_target_table": "MST_Connector",
                "suggested_target_field": "bank_name",
                "confidence_score": 88,
                "notes": "Contextual connector bank lookup",
                "lookup": _lookup("MST_Connector", "bank_name", False),
            }
        return {
            "suggested_target_table": "MST_Lender",
            "suggested_target_field": "lender_name",
            "confidence_score": 88,
            "notes": "Contextual lender name lookup",
            "lookup": _lookup("MST_Lender", "lender_name", True),
        }

    if source in {"customer_name"} and tracker_sheet:
        return {
            "suggested_target_table": "MST_Customer",
            "suggested_target_field": "full_name",
            "confidence_score": 90,
            "notes": "Tracker context customer lookup",
            "lookup": _lookup("MST_Customer", "full_name", True),
        }

    if source in {"connector", "connector_2", "connector_name_1", "connector_2_name"} and tracker_sheet:
        return {
            "suggested_target_table": "MST_Connector",
            "suggested_target_field": "full_name",
            "confidence_score": 90,
            "notes": "Tracker context connector lookup",
            "lookup": _lookup("MST_Connector", "full_name", True),
        }

    if source in {"application_number", "app_no", "app_no_", "enquiry_no", "case_no"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "case_number",
            "confidence_score": 88,
            "notes": "Tracker case identifier",
        }

    if source in {"code"} and tracker_sheet:
        return {
            "suggested_target_table": "MST_DSA",
            "suggested_target_field": "dsa_code",
            "confidence_score": 92,
            "notes": "Tracker tenant DSA code",
            "lookup": _lookup("MST_DSA", "dsa_code", False),
        }

    if source in {"branch"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "branch_name",
            "confidence_score": 82,
            "notes": "Tracker branch name",
        }

    if source in {"referred_by"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "referral_source",
            "confidence_score": 84,
            "notes": "Tracker referral source",
        }

    if source in {"entry_date"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "application_date",
            "confidence_score": 86,
            "notes": "Tracker application date",
        }

    if source in {"total_disb_amount", "disb_amt", "disburse_amt", "disb_date"} and tracker_sheet:
        if source == "disb_date":
            return {
                "suggested_target_table": "TRN_Case",
                "suggested_target_field": "disbursement_date",
                "confidence_score": 86,
                "notes": "Tracker disbursement date",
            }
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "disbursement_amount",
            "confidence_score": 86,
            "notes": "Tracker disbursement amount",
        }

    if source in {"profile"} and tracker_sheet:
        return {
            "suggested_target_table": "REF_BorrowerProfile",
            "suggested_target_field": "name",
            "confidence_score": 84,
            "notes": "Tracker borrower profile",
            "lookup": _lookup("REF_BorrowerProfile", "code", False),
        }

    if source in {"region"} and tracker_sheet:
        return {
            "suggested_target_table": "REF_Region",
            "suggested_target_field": "name",
            "confidence_score": 84,
            "notes": "Tracker region lookup",
            "lookup": _lookup("REF_Region", "code", False),
        }

    if source in {"unit_head", "sm_name", "rm_name", "entry_done_by", "payee_name_uh"} and tracker_sheet and "%" not in source_text:
        return {
            "suggested_target_table": "MST_Employee",
            "suggested_target_field": "full_name",
            "confidence_score": 85,
            "notes": "Tracker employee reference",
            "lookup": _lookup("MST_Employee", "full_name", True),
        }

    if source in {"invoice_date", "receive_date", "approval_date_1", "approval_date_2"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Commission",
            "suggested_target_field": "commission_date",
            "confidence_score": 82,
            "notes": "Tracker commission lifecycle date",
        }

    if source in {"invoice_no"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Payment",
            "suggested_target_field": "payment_number",
            "confidence_score": 80,
            "notes": "Tracker invoice reference as payment number",
        }

    if source in {"payment_request_date_c_1", "payment_request_date_c_2", "payment_request_date_c_2_1", "payment_date", "payment_date_1", "connector_2_payment_date"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Payment",
            "suggested_target_field": "payment_date",
            "confidence_score": 80,
            "notes": "Tracker payout date",
        }

    if source in {"c_1_utr", "c_2_utr"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Payment",
            "suggested_target_field": "utr_number",
            "confidence_score": 88,
            "notes": "Tracker payout UTR",
        }

    if source in {"bill_status", "payment_approval", "paid_to_unit_head", "paid_to_sm"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Commission",
            "suggested_target_field": "payment_status",
            "confidence_score": 82,
            "notes": "Tracker payout status",
        }

    if source in {"taxable_amount", "case_wise_p_l", "bank_payoutamt", "connector_payout_amt", "connector_2_payout_amt", "unit_head_amt", "sm_payout_amt"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Commission",
            "suggested_target_field": "gross_commission_amount",
            "confidence_score": 78,
            "notes": "Tracker payout gross amount",
        }

    if source in {"payment_amt", "payment_amt_1", "payment_amt_2", "connector_2_payment_amt", "final_payable_amt", "final_payable_amt_1", "final_payable_amt_2", "connector_2_final_payable_amt"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Payment",
            "suggested_target_field": "payment_amount",
            "confidence_score": 82,
            "notes": "Tracker payout payment amount",
        }

    if source in {"tds_2", "tds_2_1", "tds_2_2", "connector_2_tds_2"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Commission",
            "suggested_target_field": "tds_amount",
            "confidence_score": 82,
            "notes": "Tracker payout TDS",
        }

    if source in {"bank_payout", "connector_payout", "connector_2_payout", "unit_head", "sm_payout", "payout", "formula_percentage", "percentage_formula"} and tracker_sheet:
        return {
            "suggested_target_table": "RUL_CommissionRule",
            "suggested_target_field": "headline_percent",
            "confidence_score": 70,
            "notes": "Tracker payout percentage",
        }

    if source in {"remarks", "advance_recovery"} and tracker_sheet:
        return {
            "suggested_target_table": "TRN_Commission",
            "suggested_target_field": "notes",
            "confidence_score": 80,
            "notes": "Tracker payout notes",
        }

    if source in {"connector_code", "connector_name", "connector_pan", "connector_bank", "connector_account_no", "connector_ifsc_code", "ifsc_code", "account_no"} and connector_master_sheet:
        map_fields = {
            "connector_code": "connector_code",
            "connector_name": "full_name",
            "connector_pan": "pan",
            "connector_bank": "bank_name",
            "connector_account_no": "account_number",
            "account_no": "account_number",
            "connector_ifsc_code": "ifsc",
            "ifsc_code": "ifsc",
        }
        return {
            "suggested_target_table": "MST_Connector",
            "suggested_target_field": map_fields.get(source, "full_name"),
            "confidence_score": 93,
            "notes": "Connector bank master context",
            "lookup": _lookup("MST_Connector", map_fields.get(source, "full_name"), True),
        }

    if source in {"gst", "gstin", "connector_gst"} and connector_master_sheet:
        return {
            "suggested_target_table": "MST_Connector",
            "suggested_target_field": "gstin",
            "confidence_score": 93,
            "notes": "Connector GST context",
            "lookup": _lookup("MST_Connector", "gstin", True),
        }

    if source in {"unit_head", "sm_name", "rm_name"} and connector_master_sheet:
        return {
            "suggested_target_table": "MST_Employee",
            "suggested_target_field": "full_name",
            "confidence_score": 88,
            "notes": "Employee reference in connector master context",
            "lookup": _lookup("MST_Employee", "full_name", True),
        }

    if source in {"connector_name", "full_name"}:
        if any(token in sheet for token in {"salary", "employee"}):
            return {
                "suggested_target_table": "MST_Employee",
                "suggested_target_field": "full_name",
                "confidence_score": 88,
                "notes": "Contextual employee lookup",
                "lookup": _lookup("MST_Employee", "full_name", True),
            }
        return {
            "suggested_target_table": "MST_Connector",
            "suggested_target_field": "full_name",
            "confidence_score": 88,
            "notes": "Contextual connector lookup",
            "lookup": _lookup("MST_Connector", "full_name", True),
        }

    if source in {"company_name", "company"}:
        return {
            "suggested_target_table": "MST_Lender",
            "suggested_target_field": "lender_name",
            "confidence_score": 92,
            "notes": "Company name in lender master sheet",
            "lookup": _lookup("MST_Lender", "lender_name", True),
        }

    if source in {"product", "product_name", "lending_product"}:
        return {
            "suggested_target_table": "MST_Product",
            "suggested_target_field": "product_name",
            "confidence_score": 92,
            "notes": "Product name in lender master sheet",
            "lookup": _lookup("MST_Product", "product_name", True),
        }

    if source in {"status", "bill_status"}:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "status",
            "confidence_score": 86,
            "notes": "Status mapped with REF_Status lookup",
            "lookup": _lookup("REF_Status", "code", False),
        }

    if source in {"case_no", "case_number", "application_number", "enquiry_number"}:
        return {
            "suggested_target_table": "TRN_Case",
            "suggested_target_field": "case_number",
            "confidence_score": 90,
            "notes": "Case identifier",
        }

    if source in {"salary_range", "borrower_salary_range"}:
        return {
            "suggested_target_table": "MST_Product",
            "suggested_target_field": "borrower_salary_range",
            "confidence_score": 90,
            "notes": "Product borrower salary range",
        }

    if source in {"employer", "is_employed"}:
        return {
            "suggested_target_table": "MST_Product",
            "suggested_target_field": "is_employed",
            "confidence_score": 88,
            "notes": "Product employment attribute",
        }

    if source in {"type", "loan_type"}:
        return {
            "suggested_target_table": "REF_LoanType",
            "suggested_target_field": "name",
            "confidence_score": 86,
            "notes": "Reference loan type",
            "lookup": _lookup("REF_LoanType", "code", False),
        }

    if source in {"channel", "source_channel"}:
        return {
            "suggested_target_table": "REF_Channel",
            "suggested_target_field": "name",
            "confidence_score": 86,
            "notes": "Reference channel",
            "lookup": _lookup("REF_Channel", "code", False),
        }

    if source in {"borrower", "borrower_profile"}:
        return {
            "suggested_target_table": "REF_BorrowerProfile",
            "suggested_target_field": "name",
            "confidence_score": 86,
            "notes": "Reference borrower profile",
            "lookup": _lookup("REF_BorrowerProfile", "code", False),
        }

    if source in {"nature", "loan_nature"}:
        return {
            "suggested_target_table": "REF_LoanNature",
            "suggested_target_field": "name",
            "confidence_score": 86,
            "notes": "Reference loan nature",
            "lookup": _lookup("REF_LoanNature", "code", False),
        }

    if source in {"location", "loan_location"}:
        return {
            "suggested_target_table": "REF_Location",
            "suggested_target_field": "name",
            "confidence_score": 86,
            "notes": "Reference location",
            "lookup": _lookup("REF_Location", "code", False),
        }

    return None


def _map_commission_business_field(source_raw: str) -> tuple[str, str, int, str] | None:
    source = _normalize_header(source_raw)

    explicit_matches = {
        "slab_type": ("RUL_CommissionRule", "slab_type", 96, "Commission rule field"),
        "base": ("RUL_CommissionRule", "base_percent", 94, "Commission base percent"),
        "base_percent": ("RUL_CommissionRule", "base_percent", 95, "Commission base percent"),
        "headline": ("RUL_CommissionRule", "headline_percent", 94, "Commission headline percent"),
        "headline_percent": ("RUL_CommissionRule", "headline_percent", 95, "Commission headline percent"),
        "pf": ("RUL_CommissionRule", "pf_percent", 94, "Commission PF percent"),
        "pf_percent": ("RUL_CommissionRule", "pf_percent", 95, "Commission PF percent"),
        "i": ("RUL_CommissionRule", "i_percent", 94, "Commission insurance percent"),
        "i_percent": ("RUL_CommissionRule", "i_percent", 95, "Commission insurance percent"),
        "roi": ("MST_Product", "roi_percent", 94, "Product ROI percent"),
        "roi_percent": ("MST_Product", "roi_percent", 95, "Product ROI percent"),
        "qualifying": ("RUL_CommissionRule", "qualifying_condition", 92, "Commission qualifying condition"),
        "qualifying_notes": ("RUL_CommissionRule", "qualifying_notes", 95, "Commission qualifying notes"),
        "commercial": ("RUL_CommissionRule", "commercial_terms", 92, "Commission commercial terms"),
        "clawback": ("RUL_CommissionRule", "clawback_conditions", 92, "Commission clawback conditions"),
        "dsa": ("MST_DSA", "dsa_code", 95, "DSA tenant anchor"),
        "contest_frequency": ("RUL_Contest", "frequency", 95, "Contest frequency"),
        "contest_target": ("RUL_Contest", "target_amount", 95, "Contest target amount"),
        "contest_bonus": ("RUL_Contest", "bonus_percent", 95, "Contest bonus percent"),
        "contest_bonus_percent": ("RUL_Contest", "bonus_percent", 95, "Contest bonus percent"),
        "contest_period": ("RUL_Contest", "period", 95, "Contest period"),
        "contest_notes": ("RUL_Contest", "notes", 95, "Contest notes"),
    }

    if source in explicit_matches:
        return explicit_matches[source]

    if "dsa" in source:
        return "MST_DSA", "dsa_code", 90, "DSA tenant anchor"

    if "contest" in source:
        if "freq" in source:
            return "RUL_Contest", "frequency", 90, "Contest frequency"
        if any(token in source for token in {"target", "bonus", "period", "note"}):
            table_field = {
                "target": ("target_amount", "Contest target amount"),
                "bonus": ("bonus_percent", "Contest bonus percent"),
                "period": ("period", "Contest period"),
                "note": ("notes", "Contest notes"),
            }
            for token, (field, note) in table_field.items():
                if token in source:
                    return "RUL_Contest", field, 90, note
        return "RUL_Contest", "notes", 60, "Contest data"

    if any(token in source for token in {"slab", "tier", "rate", "bracket", "range"}):
        if any(token in source for token in {"cr", "l", "upto", "under", "above", "less", "greater", "min", "max"}):
            return "RUL_CommissionSlab", "rate", 90, "Commission slab rate"

    return None


def _annotate_context_for_column(column: dict[str, Any], source_column: str) -> None:
    source = _normalize_header(source_column)

    if source in {"lender_name", "bank_name", "connector_name", "full_name", "status", "bill_status", "case_number"}:
        return

    if "contest" in source:
        if source in {"contest_frequency", "contest_target", "contest_bonus_percent", "contest_period", "contest_notes"}:
            column.setdefault("notes", f"Contest field mapped to {column.get('suggested_target_table')}.{column.get('suggested_target_field')}")
        return

    if any(token in source for token in {"slab", "tier", "rate", "bracket", "range"}) and column.get("suggested_target_table") == "RUL_CommissionSlab":
        column["transformation"] = {
            "type": "UNPIVOT",
            "tier_min": column.get("tier_min"),
            "tier_max": column.get("tier_max"),
        }

    if column.get("suggested_target_table") == "MST_Lender" and column.get("suggested_target_field") == "lender_name":
        column.setdefault("lookup", {"table": "MST_Lender", "field": "lender_name", "create_if_missing": True})

    if column.get("suggested_target_table") == "MST_Connector" and column.get("suggested_target_field") in {"full_name", "bank_name"}:
        column.setdefault("lookup", {"table": "MST_Connector", "field": column["suggested_target_field"], "create_if_missing": True})

    if column.get("suggested_target_table") == "TRN_Case" and column.get("suggested_target_field") == "status":
        column.setdefault("lookup", {"table": "REF_Status", "field": "code", "create_if_missing": False})


def _finalize_column(column: dict[str, Any]) -> None:
    _apply_formula_context(column)
    if "confidence_level" not in column:
        column["confidence_level"] = _confidence_level(int(column.get("confidence_score") or 0))


def _propose_for_sheet(sheet: dict[str, Any], known_mappings: dict[str, Any]) -> dict[str, Any]:
    columns = sheet.get("columns", [])
    sheet_name = str(sheet.get("sheet_name") or "")
    business_context = _sheet_business_context(sheet_name, columns)
    sheet["business_domain"] = business_context.get("business_domain", [])
    sheet["business_scope"] = business_context.get("business_scope", "GENERIC")
    sheet["descoped_from"] = business_context.get("descoped_from", [])
    if business_context.get("notes"):
        sheet["notes"] = business_context["notes"]
    for col in columns:
        source_column = str(col["source_column"])
        source_norm = _normalize_header(source_column)

        if sheet["business_scope"] == "PRE_DISBURSEMENT_MIS" and source_norm in OPERATIONS_DESCOPED_COLUMNS:
            col["ignore"] = True
            col["confidence_score"] = 0
            col["notes"] = "Pre-disbursement MIS; descoped operations column"
            _finalize_column(col)
            continue

        contextual = _contextual_mapping_for_source(source_column, sheet_name, columns)
        if contextual:
            col.update(contextual)
            _annotate_context_for_column(col, source_column)
            _finalize_column(col)
            continue

        mapped = _mapping_for_source(col["source_column"], known_mappings)
        if mapped:
            table, field, score, note = mapped
            col["suggested_target_table"] = table
            col["suggested_target_field"] = field
            col["confidence_score"] = score
            col["notes"] = note
            _annotate_context_for_column(col, source_column)
            _finalize_column(col)
            continue

        commission_field = _map_commission_business_field(source_column)
        if commission_field:
            table, field, score, note = commission_field
            col["suggested_target_table"] = table
            col["suggested_target_field"] = field
            col["confidence_score"] = score
            col["notes"] = note
            _annotate_context_for_column(col, source_column)
            _finalize_column(col)
            continue

        slab_hits = detect_slab_columns([source_column])
        if source_column in slab_hits:
            col["suggested_target_table"] = slab_hits[source_column]["target_table"]
            col["suggested_target_field"] = slab_hits[source_column]["target_field"]
            col["confidence_score"] = 70
            col["notes"] = "Detected as slab column"
            col["transformation"] = {
                "type": slab_hits[source_column].get("transformation", "UNPIVOT"),
                "tier_min": slab_hits[source_column].get("tier_min"),
                "tier_max": slab_hits[source_column].get("tier_max"),
            }
            _finalize_column(col)
            continue

        if not col["suggested_target_table"]:
            if col.get("pattern") == "pan":
                col["suggested_target_table"] = "MST_Lender"
                col["suggested_target_field"] = "pan"
                col["confidence_score"] = 80
                col["notes"] = "Detected PAN pattern"
            elif col.get("pattern") == "gstin":
                col["suggested_target_table"] = "MST_Lender"
                col["suggested_target_field"] = "gstin"
                col["confidence_score"] = 80
                col["notes"] = "Detected GSTIN pattern"
                _finalize_column(col)
                continue

        if not col["suggested_target_table"]:
            if col["inferred_type"] == "percentage":
                source_hint = _normalize_header(source_column)
                if any(token in source_hint for token in {"slab", "tier", "rate", "bracket", "range"}):
                    col["suggested_target_table"] = "RUL_CommissionSlab"
                    col["suggested_target_field"] = "rate"
                    col["confidence_score"] = 40
                    col["notes"] = "Inferred slab percentage"
                    col["transformation"] = {"type": "UNPIVOT", "tier_min": None, "tier_max": None}
                else:
                    col["ignore"] = True
                    col["confidence_score"] = 0
                    col["notes"] = "Percentage needs explicit business mapping"
                _finalize_column(col)
            elif col["inferred_type"] == "amount":
                source_hint = _normalize_header(source_column)
                if any(token in source_hint for token in {"sanction", "disbursement", "loan", "amount", "ticket"}):
                    col["suggested_target_table"] = "TRN_Case"
                    col["suggested_target_field"] = "sanction_amount"
                    col["confidence_score"] = 30
                    col["notes"] = "Inferred amount type"
                else:
                    col["ignore"] = True
                    col["confidence_score"] = 0
                    col["notes"] = "Amount needs explicit business mapping"
                _finalize_column(col)

        if not col["suggested_target_table"]:
            col["ignore"] = True
            col["confidence_score"] = 0
            col["notes"] = "No mapping found"

        _finalize_column(col)

    return sheet


def generate_mapping_proposal(file_analysis: dict[str, Any], known_mappings: dict[str, Any] | None = None) -> dict[str, Any]:
    if known_mappings is None:
        known_mappings = {**KNOWN_MAPPINGS}
        for key, value in list(KNOWN_MAPPINGS.items()):
            known_mappings[_normalize_header(key)] = value

    sheets = file_analysis.get("sheets")
    if sheets:
        file_analysis["sheets"] = [_propose_for_sheet(sheet, known_mappings) for sheet in sheets]
        return file_analysis

    # Backward compatibility for single-sheet dicts.
    return _propose_for_sheet(file_analysis, known_mappings)


def apply_mapping(row: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    mapped: dict[str, Any] = {}
    for source_col, target_info in mapping.items():
        if source_col in row:
            target_table = target_info.get("target_table")
            target_field = target_info.get("target_field")
            if target_table and target_field:
                key = f"{target_table}.{target_field}"
                mapped[key] = row[source_col]
    return mapped
