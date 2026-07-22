from __future__ import annotations

from typing import Any
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from src.masters.models import (
    MST_Connector,
    MST_ConnectorBank,
    MST_Employee,
    MST_EmployeeBankAccount,
    MST_Lender,
    MST_Vendor,
)
from src.etl.services.cross_verify import CrossVerificationService, VerificationDefaults
from src.reference.models import REF_ExpenseCategory
from src.rules.models import RUL_InternalIncentiveScheme
from src.transactions.models import (
    ETL_RedFlag,
    TRN_BankStatementLine,
    TRN_Case,
    TRN_CaseConnectorSplit,
    TRN_Commission,
    TRN_Expense,
    TRN_IncentiveEarned,
    TRN_Invoice,
    TRN_Revenue,
    TRN_Salary,
    TRN_StatutoryPayment,
)


def _promote_simple(
    session: Session,
    staging_rows: list[dict],
    model: Any,
    pk_field: str,
    natural_keys: list[str],
    required_fields: list[str] | None = None,
    conflict_resolution: str = "SKIP",
) -> dict:
    created = 0
    updated = 0
    skipped = 0
    failed = 0
    records: list[tuple[dict, int]] = []
    required_fields = required_fields or []

    table_fields = {col.name for col in model.__table__.columns}
    date_fields = {col.name for col in model.__table__.columns if getattr(col.type, "python_type", None) is date}

    def _coerce_value(field: str, value: Any) -> Any:
        if field not in date_fields:
            return value
        if value in (None, ""):
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        text = str(value).strip()
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
            try:
                return datetime.strptime(text, fmt).date()
            except Exception:
                pass
        try:
            return datetime.fromisoformat(text).date()
        except Exception:
            return None

    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if any(row_data.get(req) in (None, "") for req in required_fields):
            failed += 1
            continue

        valid_data = {
            k: _coerce_value(k, v)
            for k, v in row_data.items()
            if k in table_fields and v not in (None, "")
        }
        valid_data = {k: v for k, v in valid_data.items() if v is not None}

        existing = None
        filters = {k: row_data.get(k) for k in natural_keys if row_data.get(k) not in (None, "")}
        if filters:
            existing = session.query(model).filter_by(**filters).first()

        if existing:
            if conflict_resolution == "SKIP":
                skipped += 1
                records.append((item, getattr(existing, pk_field)))
                continue
            if conflict_resolution == "FAIL":
                failed += 1
                continue

            for k, v in valid_data.items():
                setattr(existing, k, v)
            if "is_active" in table_fields:
                setattr(existing, "is_active", True)
            session.add(existing)
            session.flush()
            updated += 1
            records.append((item, getattr(existing, pk_field)))
            continue

        if "is_active" in table_fields and "is_active" not in valid_data:
            valid_data["is_active"] = True

        created_obj = model(**valid_data)
        session.add(created_obj)
        session.flush()
        created += 1
        records.append((item, getattr(created_obj, pk_field)))

    return {
        "table": model.__tablename__,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "failed": failed,
        "records": records,
    }


def promote_connector(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if row_data.get("full_name") in (None, ""):
            row_data["full_name"] = row_data.get("connector_name")
        if row_data.get("connector_name") in (None, ""):
            row_data["connector_name"] = row_data.get("full_name")
        item["mapped_data"] = row_data
    return _promote_simple(session, staging_rows, MST_Connector, "connector_id", ["connector_code", "pan"], ["full_name"], conflict_resolution)


def promote_connector_bank(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, MST_ConnectorBank, "connector_bank_id", ["connector_id", "account_number"], [], conflict_resolution)


def promote_employee(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, MST_Employee, "employee_id", ["employee_code"], ["full_name"], conflict_resolution)


def promote_employee_bank_account(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, MST_EmployeeBankAccount, "employee_bank_account_id", ["employee_id", "account_number"], [], conflict_resolution)


def promote_vendor(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, MST_Vendor, "vendor_id", ["vendor_name"], ["vendor_name"], conflict_resolution)


def promote_expense_category_ref(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if row_data.get("name") in (None, ""):
            row_data["name"] = row_data.get("category_name")
        if row_data.get("code") in (None, "") and row_data.get("name") not in (None, ""):
            row_data["code"] = str(row_data["name"]).strip().upper().replace(" ", "_")[:100]
        item["mapped_data"] = row_data
    return _promote_simple(session, staging_rows, REF_ExpenseCategory, "id", ["code"], ["name", "code"], conflict_resolution)


def promote_case(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        row_data.setdefault("customer_id", 0)
        row_data.setdefault("lender_id", 0)
        row_data.setdefault("product_id", 0)
        item["mapped_data"] = row_data
    return _promote_simple(session, staging_rows, TRN_Case, "case_id", ["case_number"], ["case_number"], conflict_resolution)


def promote_revenue(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if row_data.get("revenue_date") in (None, ""):
            row_data["revenue_date"] = date.today()
        if row_data.get("net_amount") in (None, ""):
            row_data["net_amount"] = row_data.get("gross_amount") or row_data.get("amount") or 0.0
        item["mapped_data"] = row_data

    result = _promote_simple(session, staging_rows, TRN_Revenue, "revenue_id", ["case_id", "utr_number"], ["net_amount"], conflict_resolution)

    verifier = CrossVerificationService()
    generated_flags = 0
    for row_wrapper, revenue_id in result.get("records", []):
        row_data = dict(row_wrapper.get("mapped_data", {}))
        staging_row = row_wrapper.get("staging_row")
        revenue = session.query(TRN_Revenue).filter(TRN_Revenue.revenue_id == revenue_id).first()
        if revenue is None:
            continue

        defaults = VerificationDefaults(
            default_gst_rate=Decimal(str(row_data.get("default_gst_rate", 0) or 0)),
            default_tds_rate=Decimal(str(row_data.get("default_tds_rate", 0) or 0)),
        )
        if revenue.case_id:
            case = session.query(TRN_Case).filter(TRN_Case.case_id == revenue.case_id).first()
            if case and case.lender_id:
                lender = session.query(MST_Lender).filter(MST_Lender.lender_id == case.lender_id).first()
                if lender:
                    defaults.default_gst_rate = Decimal(str(lender.default_gst_rate or defaults.default_gst_rate))
                    defaults.default_tds_rate = Decimal(str(lender.default_tds_rate or defaults.default_tds_rate))

        verification = verifier.verify_revenue(row_data, defaults)
        revenue.party_id = revenue.party_id or row_data.get("party_id")
        revenue.reported_amount = verification["reported_amount"]
        revenue.reported_gst = verification["reported_gst"]
        revenue.reported_tds = verification["reported_tds"]
        revenue.reported_net = verification["reported_net"]
        revenue.system_gst = verification["system_gst"]
        revenue.system_tds = verification["system_tds"]
        revenue.gst_match = verification["gst_match"]
        revenue.tds_match = verification["tds_match"]
        if not revenue.data:
            revenue.data = {}

        for flag_payload in verification["red_flags"]:
            session.add(
                verifier.build_red_flag(
                    company_id=staging_row.company_id if staging_row is not None else revenue.company_id,
                    batch_guid=getattr(staging_row, "batch_guid", None),
                    record_type="revenue",
                    record_id=revenue.revenue_id,
                    payload=flag_payload,
                )
            )
            generated_flags += 1

    if generated_flags:
        result["red_flags"] = generated_flags
    return result


def promote_commission_txn(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if row_data.get("commission_date") in (None, ""):
            row_data["commission_date"] = date.today()
        if row_data.get("net_amount") in (None, ""):
            row_data["net_amount"] = row_data.get("gross_amount") or row_data.get("amount") or 0.0
        item["mapped_data"] = row_data

    result = _promote_simple(session, staging_rows, TRN_Commission, "commission_id", ["case_id", "connector_id", "utr_number"], ["net_amount"], conflict_resolution)

    verifier = CrossVerificationService()
    generated_flags = 0
    for row_wrapper, commission_id in result.get("records", []):
        row_data = dict(row_wrapper.get("mapped_data", {}))
        staging_row = row_wrapper.get("staging_row")
        commission = session.query(TRN_Commission).filter(TRN_Commission.commission_id == commission_id).first()
        if commission is None:
            continue

        defaults = VerificationDefaults(
            default_gst_rate=Decimal(str(row_data.get("default_gst_rate", 0) or 0)),
            default_tds_rate=Decimal(str(row_data.get("default_tds_rate", 0) or 0)),
            max_commission=Decimal(str(row_data.get("max_commission"))) if row_data.get("max_commission") not in (None, "") else None,
        )
        if commission.connector_id:
            connector = session.query(MST_Connector).filter(MST_Connector.connector_id == commission.connector_id).first()
            if connector:
                defaults.default_gst_rate = Decimal(str(connector.default_gst_rate or defaults.default_gst_rate))
                defaults.default_tds_rate = Decimal(str(connector.default_tds_rate or defaults.default_tds_rate))
                if connector.max_commission is not None:
                    defaults.max_commission = Decimal(str(connector.max_commission))

        verification = verifier.verify_commission(row_data, defaults)
        commission.party_id = commission.party_id or row_data.get("party_id")
        commission.reported_commission = verification["reported_commission"]
        commission.reported_gst = verification["reported_gst"]
        commission.reported_tds = verification["reported_tds"]
        commission.reported_net = verification["reported_net"]
        commission.gst_match = verification["gst_match"]
        commission.tds_match = verification["tds_match"]
        commission.exceeds_max = verification["exceeds_max"]
        if not commission.data:
            commission.data = {}

        for flag_payload in verification["red_flags"]:
            session.add(
                verifier.build_red_flag(
                    company_id=staging_row.company_id if staging_row is not None else commission.company_id,
                    batch_guid=getattr(staging_row, "batch_guid", None),
                    record_type="commission",
                    record_id=commission.commission_id,
                    payload=flag_payload,
                )
            )
            generated_flags += 1

    if generated_flags:
        result["red_flags"] = generated_flags
    return result


def promote_case_connector_split(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_CaseConnectorSplit, "split_id", ["case_id", "connector_id"], ["case_id"], conflict_resolution)


def promote_incentive_earned(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_IncentiveEarned, "incentive_earned_id", ["case_id", "employee_id"], [], conflict_resolution)


def promote_invoice(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_Invoice, "invoice_id", ["invoice_number", "application_number"], [], conflict_resolution)


def promote_salary(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_Salary, "salary_id", ["employee_id", "pay_month"], [], conflict_resolution)


def promote_statutory_payment(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_StatutoryPayment, "statutory_payment_id", ["salary_id"], [], conflict_resolution)


def promote_expense(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    for item in staging_rows:
        row_data = dict(item.get("mapped_data", {}))
        if row_data.get("expense_date") in (None, ""):
            row_data["expense_date"] = row_data.get("invoice_date") or row_data.get("payment_date") or date.today()
        if row_data.get("net_amount") in (None, ""):
            row_data["net_amount"] = row_data.get("gross_amount") or row_data.get("amount") or 0.0
        if row_data.get("amount") in (None, ""):
            row_data["amount"] = row_data.get("gross_amount") or row_data.get("net_amount") or 0.0
        if row_data.get("invoice_reference") in (None, ""):
            row_data["invoice_reference"] = row_data.get("utr_number")
        item["mapped_data"] = row_data
    return _promote_simple(session, staging_rows, TRN_Expense, "expense_id", ["invoice_reference", "utr_number"], ["net_amount"], conflict_resolution)


def promote_bank_statement_line(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(session, staging_rows, TRN_BankStatementLine, "statement_line_id", ["utr_number", "transaction_date"], ["bank_name"], conflict_resolution)


def promote_internal_incentive_scheme(session: Session, staging_rows: list[dict], template: object, conflict_resolution: str = "SKIP") -> dict:
    return _promote_simple(
        session,
        staging_rows,
        RUL_InternalIncentiveScheme,
        "incentive_id",
        ["employee_id", "type", "effective_from"],
        ["employee_id", "type"],
        conflict_resolution,
    )
