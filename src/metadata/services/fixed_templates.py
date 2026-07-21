from __future__ import annotations

from typing import TypedDict


class FixedTemplateOption(TypedDict):
    template_name: str
    label: str
    primary_table: str


FIXED_TEMPLATE_OPTIONS: list[FixedTemplateOption] = [
    {
        "template_name": "MIS_TEMPLATE_LenderMaster.xlsx",
        "label": "Lender Master",
        "primary_table": "MST_Lender",
    },
    {
        "template_name": "MIS_TEMPLATE_ConnectorMaster.xlsx",
        "label": "Connector Master",
        "primary_table": "MST_Connector",
    },
    {
        "template_name": "MIS_TEMPLATE_SecuredTracker.xlsx",
        "label": "Secured Tracker",
        "primary_table": "TRN_Case",
    },
    {
        "template_name": "MIS_TEMPLATE_UnsecuredTracker.xlsx",
        "label": "Unsecured Tracker",
        "primary_table": "TRN_Case",
    },
    {
        "template_name": "MIS_TEMPLATE_Employee_Master.xlsx",
        "label": "Employee Master",
        "primary_table": "MST_Employee",
    },
    {
        "template_name": "MIS_TEMPLATE_Salary_Details.xlsx",
        "label": "Salary Details",
        "primary_table": "TRN_Salary",
    },
    {
        "template_name": "MIS_TEMPLATE_Employee_Incentive_Master.xlsx",
        "label": "Employee Incentive Master",
        "primary_table": "RUL_InternalIncentiveScheme",
    },
    {
        "template_name": "MIS_TEMPLATE_Expense_Payment_Tracker.xlsx",
        "label": "Expense Payment Tracker",
        "primary_table": "TRN_Expense",
    },
    {
        "template_name": "MIS_TEMPLATE_Invoice_Dump.xlsx",
        "label": "Invoice Dump",
        "primary_table": "TRN_Invoice",
    },
    {
        "template_name": "MIS_TEMPLATE_Bank_Statement.xlsx",
        "label": "Bank Statement",
        "primary_table": "TRN_BankStatementLine",
    },
]


FIXED_TEMPLATE_NAME_SET = {item["template_name"] for item in FIXED_TEMPLATE_OPTIONS}
FIXED_TEMPLATE_PRIMARY_TABLE = {item["template_name"]: item["primary_table"] for item in FIXED_TEMPLATE_OPTIONS}
