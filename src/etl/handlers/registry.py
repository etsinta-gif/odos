from src.etl.handlers.commission_rule import promote_commission_rule
from src.etl.handlers.commission_slab import promote_commission_slab
from src.etl.handlers.contest import promote_contest
from src.etl.handlers.lender import promote_lender
from src.etl.handlers.product import promote_product
from src.etl.handlers.simple import (
    promote_bank_statement_line,
    promote_case,
    promote_case_connector_split,
    promote_commission_txn,
    promote_connector,
    promote_connector_bank,
    promote_employee,
    promote_employee_bank_account,
    promote_expense,
    promote_expense_category_ref,
    promote_incentive_earned,
    promote_internal_incentive_scheme,
    promote_invoice,
    promote_revenue,
    promote_salary,
    promote_statutory_payment,
    promote_vendor,
)


HANDLER_REGISTRY = {
    "MST_Lender": {
        "handler": promote_lender,
        "natural_key": ["lender_code", "pan"],
        "parent_tables": [],
    },
    "MST_Product": {
        "handler": promote_product,
        "natural_key": ["product_code", "lender_code"],
        "parent_tables": ["MST_Lender"],
    },
    "RUL_CommissionRule": {
        "handler": promote_commission_rule,
        "natural_key": ["lender_code", "product_code", "slab_type"],
        "parent_tables": ["MST_Lender", "MST_Product"],
    },
    "RUL_CommissionSlab": {
        "handler": promote_commission_slab,
        "natural_key": ["lender_code", "product_code", "slab_type", "tier_name"],
        "parent_tables": ["RUL_CommissionRule"],
    },
    "RUL_Contest": {
        "handler": promote_contest,
        "natural_key": ["contest_code"],
        "parent_tables": [],
    },
    "MST_Connector": {
        "handler": promote_connector,
        "natural_key": ["connector_code", "pan"],
        "parent_tables": [],
    },
    "MST_ConnectorBank": {
        "handler": promote_connector_bank,
        "natural_key": ["connector_id", "account_number"],
        "parent_tables": ["MST_Connector"],
    },
    "MST_Employee": {
        "handler": promote_employee,
        "natural_key": ["employee_code"],
        "parent_tables": [],
    },
    "MST_EmployeeBankAccount": {
        "handler": promote_employee_bank_account,
        "natural_key": ["employee_id", "account_number"],
        "parent_tables": ["MST_Employee"],
    },
    "MST_Vendor": {
        "handler": promote_vendor,
        "natural_key": ["vendor_name"],
        "parent_tables": [],
    },
    "REF_ExpenseCategory": {
        "handler": promote_expense_category_ref,
        "natural_key": ["name", "code"],
        "parent_tables": [],
    },
    "TRN_Case": {
        "handler": promote_case,
        "natural_key": ["case_number"],
        "parent_tables": [],
    },
    "TRN_Revenue": {
        "handler": promote_revenue,
        "natural_key": ["case_id", "utr_number"],
        "parent_tables": ["TRN_Case"],
    },
    "TRN_Commission": {
        "handler": promote_commission_txn,
        "natural_key": ["case_id", "connector_id", "utr_number"],
        "parent_tables": ["TRN_Case"],
    },
    "TRN_CaseConnectorSplit": {
        "handler": promote_case_connector_split,
        "natural_key": ["case_id", "connector_id"],
        "parent_tables": ["TRN_Case", "MST_Connector"],
    },
    "TRN_IncentiveEarned": {
        "handler": promote_incentive_earned,
        "natural_key": ["case_id", "employee_id"],
        "parent_tables": ["TRN_Case", "MST_Employee"],
    },
    "TRN_Invoice": {
        "handler": promote_invoice,
        "natural_key": ["invoice_number", "application_number"],
        "parent_tables": ["TRN_Case"],
    },
    "TRN_Salary": {
        "handler": promote_salary,
        "natural_key": ["employee_id", "pay_month"],
        "parent_tables": ["MST_Employee"],
    },
    "TRN_StatutoryPayment": {
        "handler": promote_statutory_payment,
        "natural_key": ["salary_id"],
        "parent_tables": ["TRN_Salary"],
    },
    "TRN_Expense": {
        "handler": promote_expense,
        "natural_key": ["invoice_reference", "utr_number"],
        "parent_tables": ["MST_Vendor", "REF_ExpenseCategory"],
    },
    "TRN_BankStatementLine": {
        "handler": promote_bank_statement_line,
        "natural_key": ["utr_number", "transaction_date"],
        "parent_tables": [],
    },
    "RUL_InternalIncentiveScheme": {
        "handler": promote_internal_incentive_scheme,
        "natural_key": ["employee_id", "type", "effective_from"],
        "parent_tables": ["MST_Employee"],
    },
}


def get_handler(table_name: str):
    return HANDLER_REGISTRY.get(table_name)


def get_tables_in_order() -> list[str]:
    remaining = {table: set(info["parent_tables"]) for table, info in HANDLER_REGISTRY.items()}
    order: list[str] = []

    while remaining:
        ready = sorted(table for table, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError("Circular dependency detected in multi-target handler registry")
        for table in ready:
            order.append(table)
            remaining.pop(table)
        for deps in remaining.values():
            deps.difference_update(ready)

    return order