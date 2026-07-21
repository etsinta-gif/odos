from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.masters.models import (
    MST_CompanyBankAccount,
    MST_CostCenter,
    MST_Customer,
    MST_Employee,
    MST_ExpenseCategory,
    MST_Vendor,
)
from src.transactions.models import (
    ETL_DataLineage,
    ETL_ErrorLog,
    ETL_ImportBatch,
    ETL_StagingRawData,
    TRN_Case,
    TRN_Commission,
    TRN_Expense,
    TRN_ExpenseClaim,
    TRN_Payment,
    TRN_RecurringExpense,
    TRN_Revenue,
)
from src.security.auth import get_current_user
from src.security.models import SEC_User

router = APIRouter(prefix="/masters/data", tags=["Data Ops UI"], dependencies=[Depends(get_current_user)])
TEMPLATES = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")

RAW_DATASETS = {
    "customers": (MST_Customer, ["customer_id", "full_name", "pan", "email", "mobile", "is_active"]),
    "employees": (MST_Employee, ["employee_id", "employee_code", "full_name", "designation", "department", "is_active"]),
    "vendors": (MST_Vendor, ["vendor_id", "vendor_name", "is_active"]),
    "expense-categories": (MST_ExpenseCategory, ["expense_category_id", "category_name", "is_active"]),
    "cost-centers": (MST_CostCenter, ["cost_center_id", "center_name", "is_active"]),
    "company-bank-accounts": (MST_CompanyBankAccount, ["bank_account_id", "bank_name", "account_number", "ifsc", "is_active"]),
    "cases": (TRN_Case, ["case_id", "case_number", "customer_id", "lender_id", "product_id", "status", "is_active"]),
    "revenue": (TRN_Revenue, ["revenue_id", "case_id", "base_revenue_amount", "gst_amount", "tds_amount", "net_amount", "payment_status", "is_active"]),
    "commission": (TRN_Commission, ["commission_id", "case_id", "connector_id", "base_commission_amount", "gst_amount", "tds_amount", "net_amount", "payment_status", "is_active"]),
    "expenses": (TRN_Expense, ["expense_id", "expense_date", "vendor_id", "expense_category_id", "amount", "gst_amount", "tds_amount", "net_amount", "payment_status", "is_active"]),
    "payments": (TRN_Payment, ["payment_id", "payment_number", "payment_date", "payment_amount", "payment_type", "payment_mode", "reconciliation_status", "is_active"]),
    "recurring-expenses": (TRN_RecurringExpense, ["recurring_expense_id", "frequency", "amount", "gst_amount", "tds_amount", "net_amount", "is_active"]),
    "expense-claims": (TRN_ExpenseClaim, ["expense_claim_id", "employee_id", "amount", "status", "is_active"]),
    "etl-batches": (ETL_ImportBatch, ["batch_id", "batch_guid", "template_id", "file_name", "import_status", "total_rows", "successful_rows", "failed_rows"]),
    "etl-staging": (ETL_StagingRawData, ["staging_id", "batch_guid", "table_name", "source_row_number", "validation_status", "is_promoted"]),
    "etl-errors": (ETL_ErrorLog, ["error_id", "batch_guid", "table_name", "error_type", "error_message", "error_datetime"]),
    "etl-lineage": (ETL_DataLineage, ["lineage_id", "batch_guid", "staging_id", "target_table", "target_id", "created_at"]),
}


def _company_scoped_query(db: Session, model, company_id: int):
    query = db.query(model)
    if hasattr(model, "company_id"):
        query = query.filter(model.company_id == company_id)
    return query


@router.get("/overview")
def data_overview(request: Request, current_user: SEC_User = Depends(get_current_user), db: Session = Depends(get_db)):
    counts = []
    for key, (model, _) in RAW_DATASETS.items():
        counts.append({"dataset": key, "rows": _company_scoped_query(db, model, current_user.company_id).count()})

    return TEMPLATES.TemplateResponse(
        "masters/data_overview.html",
        {
            "request": request,
            "counts": counts,
            "raw_datasets": sorted(RAW_DATASETS.keys()),
        },
    )


@router.get("/raw/{dataset}")
def raw_dataset_view(
    request: Request,
    dataset: str,
    limit: int = Query(200, ge=1, le=1000),
    current_user: SEC_User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if dataset not in RAW_DATASETS:
        raise HTTPException(status_code=404, detail="Dataset not found")

    model, columns = RAW_DATASETS[dataset]
    rows_query = _company_scoped_query(db, model, current_user.company_id)
    rows = rows_query.limit(limit).all()

    flat_rows = []
    for row in rows:
        item = {}
        for col in columns:
            item[col] = getattr(row, col, None)
        flat_rows.append(item)

    return TEMPLATES.TemplateResponse(
        "masters/data_raw_list.html",
        {
            "request": request,
            "dataset": dataset,
            "columns": columns,
            "rows": flat_rows,
            "limit": limit,
            "total": rows_query.count(),
        },
    )


@router.get("/tax-summary")
def tax_summary(request: Request, current_user: SEC_User = Depends(get_current_user), db: Session = Depends(get_db)):
    summary = {
        "revenue": {
            "rows": db.query(TRN_Revenue).filter(TRN_Revenue.company_id == current_user.company_id).count(),
            "gst_sum": db.query(func.coalesce(func.sum(TRN_Revenue.gst_amount), 0.0)).filter(TRN_Revenue.company_id == current_user.company_id).scalar(),
            "tds_sum": db.query(func.coalesce(func.sum(TRN_Revenue.tds_amount), 0.0)).filter(TRN_Revenue.company_id == current_user.company_id).scalar(),
            "net_sum": db.query(func.coalesce(func.sum(TRN_Revenue.net_amount), 0.0)).filter(TRN_Revenue.company_id == current_user.company_id).scalar(),
        },
        "commission": {
            "rows": db.query(TRN_Commission).filter(TRN_Commission.company_id == current_user.company_id).count(),
            "gst_sum": db.query(func.coalesce(func.sum(TRN_Commission.gst_amount), 0.0)).filter(TRN_Commission.company_id == current_user.company_id).scalar(),
            "tds_sum": db.query(func.coalesce(func.sum(TRN_Commission.tds_amount), 0.0)).filter(TRN_Commission.company_id == current_user.company_id).scalar(),
            "net_sum": db.query(func.coalesce(func.sum(TRN_Commission.net_amount), 0.0)).filter(TRN_Commission.company_id == current_user.company_id).scalar(),
        },
        "expense": {
            "rows": db.query(TRN_Expense).filter(TRN_Expense.company_id == current_user.company_id).count(),
            "gst_sum": db.query(func.coalesce(func.sum(TRN_Expense.gst_amount), 0.0)).filter(TRN_Expense.company_id == current_user.company_id).scalar(),
            "tds_sum": db.query(func.coalesce(func.sum(TRN_Expense.tds_amount), 0.0)).filter(TRN_Expense.company_id == current_user.company_id).scalar(),
            "net_sum": db.query(func.coalesce(func.sum(TRN_Expense.net_amount), 0.0)).filter(TRN_Expense.company_id == current_user.company_id).scalar(),
        },
    }

    return TEMPLATES.TemplateResponse(
        "masters/data_tax_summary.html",
        {
            "request": request,
            "summary": summary,
        },
    )
