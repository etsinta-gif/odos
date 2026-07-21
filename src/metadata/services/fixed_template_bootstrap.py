from __future__ import annotations

import json
from datetime import datetime

from sqlalchemy.orm import Session

from src.metadata.models import META_FieldMapping, META_ImportTemplate


def _mapping(source_column: str, target_table: str, target_field: str, confidence: int = 95) -> dict:
    return {
        "source_column": source_column,
        "target_table": target_table,
        "target_field": target_field,
        "confidence_score": confidence,
        "is_verified": True,
        "is_natural_key": source_column.strip().lower() in {"case number", "employee code", "connector code", "lender / nbfc", "invoice number"},
        "transformation_rule": None,
        "notes": "Fixed approved template",
    }


FIXED_TEMPLATE_SPECS = [
    {
        "template_name": "MIS_TEMPLATE_LenderMaster.xlsx",
        "sheet_name": "Master",
        "header_row": 1,
        "file_pattern": r".*LenderMaster.*\\.xlsx",
        "mappings": [
            _mapping("Lender / NBFC", "MST_Lender", "lender_name"),
            _mapping("NBFC?", "MST_Lender", "is_nbfc"),
            _mapping("PAN", "MST_Lender", "pan"),
            _mapping("GST", "MST_Lender", "gstin"),
            _mapping("Category", "MST_Product", "category"),
            _mapping("Sub-product", "MST_Product", "sub_product"),
            _mapping("Type", "REF_LoanType", "name"),
            _mapping("Slab Type", "RUL_CommissionRule", "slab_type"),
            _mapping("Base %", "RUL_CommissionRule", "base_percent"),
            _mapping("< ₹50 L", "RUL_CommissionSlab", "rate"),
            _mapping("₹50 L – < ₹1 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹1 Cr – < ₹2 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹2 Cr – < ₹3 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹3 Cr – < ₹5 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹5 Cr – < ₹10 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹10 Cr – < ₹25 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹25 Cr – < ₹50 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("₹50 Cr – < ₹100 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("≥ ₹100 Cr", "RUL_CommissionSlab", "rate"),
            _mapping("Clawback Period", "RUL_CommissionRule", "clawback_period_months"),
            _mapping("Clawback %", "RUL_CommissionRule", "clawback_percent"),
            _mapping("Contest Frequency", "RUL_Contest", "frequency"),
            _mapping("Contest Target (₹)", "RUL_Contest", "target_amount"),
            _mapping("Contest Bonus %", "RUL_Contest", "bonus_percent"),
            _mapping("Contest Period", "RUL_Contest", "period"),
            _mapping("Contest Notes", "RUL_Contest", "notes"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_ConnectorMaster.xlsx",
        "sheet_name": "Master",
        "header_row": 1,
        "file_pattern": r".*ConnectorMaster.*\\.xlsx",
        "mappings": [
            _mapping("Connector Code", "MST_Connector", "connector_code"),
            _mapping("Connector Name", "MST_Connector", "full_name"),
            _mapping("PAN", "MST_Connector", "pan"),
            _mapping("GST", "MST_Connector", "gstin"),
            _mapping("Bank Name", "MST_ConnectorBank", "bank_name"),
            _mapping("Account Number", "MST_ConnectorBank", "account_number"),
            _mapping("IFSC Code", "MST_ConnectorBank", "ifsc_code"),
            _mapping("Slab Type", "RUL_CommissionRule", "slab_type"),
            _mapping("Default Share %", "RUL_CommissionRule", "connector_share_percent"),
            _mapping("< ₹50 L", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹50 L – < ₹1 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹1 Cr – < ₹2 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹2 Cr – < ₹3 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹3 Cr – < ₹5 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹5 Cr – < ₹10 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹10 Cr – < ₹25 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹25 Cr – < ₹50 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("₹50 Cr – < ₹100 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("≥ ₹100 Cr", "RUL_CommissionSlab", "connector_share"),
            _mapping("Contest Frequency", "RUL_Contest", "frequency"),
            _mapping("Contest Target (₹)", "RUL_Contest", "target_amount"),
            _mapping("Contest Bonus %", "RUL_Contest", "bonus_percent"),
            _mapping("Contest Period", "RUL_Contest", "period"),
            _mapping("Contest Notes", "RUL_Contest", "notes"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_SecuredTracker.xlsx",
        "sheet_name": "Tracker",
        "header_row": 1,
        "file_pattern": r".*SecuredTracker.*\\.xlsx",
        "mappings": [
            _mapping("Case Number", "TRN_Case", "case_number"),
            _mapping("Customer Name", "TRN_Case", "customer_name"),
            _mapping("Company Name", "TRN_Case", "company_name"),
            _mapping("Lender / NBFC", "TRN_Case", "lender_id"),
            _mapping("Category", "TRN_Case", "product_id"),
            _mapping("Sub-product", "TRN_Case", "product_id"),
            _mapping("Region", "TRN_Case", "region_id"),
            _mapping("Total Disb Amount", "TRN_Case", "total_disbursement_amount"),
            _mapping("Disbursement Date", "TRN_Case", "disbursement_date"),
            _mapping("Status", "TRN_Case", "status"),
            _mapping("Cancelled", "TRN_Case", "is_cancelled"),
            _mapping("Remarks", "TRN_Case", "remarks"),
            _mapping("Bank Payout Rate %", "TRN_Revenue", "rate_percent"),
            _mapping("Bank Payout Gross", "TRN_Revenue", "gross_amount"),
            _mapping("Bank Payout GST", "TRN_Revenue", "gst_amount"),
            _mapping("Bank Payout TDS", "TRN_Revenue", "tds_amount"),
            _mapping("Bank Payout Net", "TRN_Revenue", "net_amount"),
            _mapping("Connector Code", "TRN_Commission", "connector_id"),
            _mapping("Share %", "TRN_CaseConnectorSplit", "share_percent"),
            _mapping("Connector Payout Rate %", "TRN_Commission", "rate_percent"),
            _mapping("Connector Payout Gross", "TRN_Commission", "gross_amount"),
            _mapping("Connector Payout GST", "TRN_Commission", "gst_amount"),
            _mapping("Connector Payout TDS", "TRN_Commission", "tds_amount"),
            _mapping("Connector Payout Net", "TRN_Commission", "net_amount"),
            _mapping("Payment Request Date", "TRN_Commission", "payment_request_date"),
            _mapping("Payment Paid Date", "TRN_Commission", "payment_paid_date"),
            _mapping("UTR Number", "TRN_Commission", "utr_number"),
            _mapping("Advance Paid", "TRN_Commission", "advance_paid"),
            _mapping("Advance Date", "TRN_Commission", "advance_date"),
            _mapping("Recovery Made", "TRN_Commission", "recovery_made"),
            _mapping("Recovery Date", "TRN_Commission", "recovery_date"),
            _mapping("Unit Head Name", "TRN_Case", "unit_head_id"),
            _mapping("Unit Head Incentive %", "TRN_IncentiveEarned", "incentive_percent"),
            _mapping("Unit Head Incentive Amount", "TRN_IncentiveEarned", "amount"),
            _mapping("SM Name", "TRN_Case", "sales_manager_id"),
            _mapping("SM Incentive %", "TRN_IncentiveEarned", "incentive_percent"),
            _mapping("SM Incentive Amount", "TRN_IncentiveEarned", "amount"),
            _mapping("Invoice Number", "TRN_Invoice", "invoice_number"),
            _mapping("Invoice Date", "TRN_Invoice", "invoice_date"),
            _mapping("Invoice Due Date", "TRN_Invoice", "due_date"),
            _mapping("Invoice Received Date", "TRN_Invoice", "received_date"),
            _mapping("Invoice UTR", "TRN_Invoice", "utr_number"),
            _mapping("Confirmed by Bank Date", "TRN_Case", "confirmed_by_bank_date"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_UnsecuredTracker.xlsx",
        "sheet_name": "Tracker",
        "header_row": 1,
        "file_pattern": r".*UnsecuredTracker.*\\.xlsx",
        "mappings": [],
    },
    {
        "template_name": "MIS_TEMPLATE_Employee_Master.xlsx",
        "sheet_name": "Employees",
        "header_row": 1,
        "file_pattern": r".*Employee_Master.*\\.xlsx",
        "mappings": [
            _mapping("Employee Code", "MST_Employee", "employee_code"),
            _mapping("Employee Name", "MST_Employee", "full_name"),
            _mapping("Gender", "MST_Employee", "gender"),
            _mapping("DOB", "MST_Employee", "date_of_birth"),
            _mapping("PAN", "MST_Employee", "pan"),
            _mapping("Bank Name", "MST_EmployeeBankAccount", "bank_name"),
            _mapping("Account Number", "MST_EmployeeBankAccount", "account_number"),
            _mapping("IFSC", "MST_EmployeeBankAccount", "ifsc_code"),
            _mapping("Date of Joining", "MST_Employee", "date_of_joining"),
            _mapping("Designation", "MST_Employee", "designation"),
            _mapping("Department", "MST_Employee", "department"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_Salary_Details.xlsx",
        "sheet_name": "Salary",
        "header_row": 1,
        "file_pattern": r".*Salary_Details.*\\.xlsx",
        "mappings": [
            _mapping("Employee Code", "TRN_Salary", "employee_id"),
            _mapping("Pay Month", "TRN_Salary", "pay_month"),
            _mapping("Basic + DA", "TRN_Salary", "basic_da"),
            _mapping("HRA", "TRN_Salary", "hra"),
            _mapping("Other Allowance", "TRN_Salary", "other_allowance"),
            _mapping("Gross Earnings", "TRN_Salary", "gross_earnings"),
            _mapping("Commission Earned", "TRN_Salary", "commission_amount"),
            _mapping("Include Commission in Tax", "TRN_Salary", "include_commission_in_tax"),
            _mapping("Total Earnings", "TRN_Salary", "total_earnings"),
            _mapping("PF - Employee", "TRN_StatutoryPayment", "pf_employee_share"),
            _mapping("PF - Employer", "TRN_StatutoryPayment", "pf_employer_share"),
            _mapping("ESIC - Employee", "TRN_StatutoryPayment", "esic_employee_share"),
            _mapping("ESIC - Employer", "TRN_StatutoryPayment", "esic_employer_share"),
            _mapping("Professional Tax", "TRN_StatutoryPayment", "professional_tax"),
            _mapping("TDS", "TRN_StatutoryPayment", "tds_amount"),
            _mapping("Advance Salary", "TRN_Salary", "advance_salary"),
            _mapping("Net Payable", "TRN_Salary", "net_payable"),
            _mapping("UTR Number", "TRN_Salary", "utr_number"),
            _mapping("Payment Date", "TRN_Salary", "payment_date"),
            _mapping("Tagged Employee Code", "TRN_Salary", "tagged_employee_id"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_Employee_Incentive_Master.xlsx",
        "sheet_name": "Incentives",
        "header_row": 1,
        "file_pattern": r".*Employee_Incentive_Master.*\\.xlsx",
        "mappings": [
            _mapping("Employee Code", "MST_Employee", "employee_code"),
            _mapping("Incentive Type", "RUL_InternalIncentiveScheme", "type"),
            _mapping("Calculation Basis", "RUL_InternalIncentiveScheme", "basis"),
            _mapping("Incentive % / Amount", "RUL_InternalIncentiveScheme", "rate"),
            _mapping("Slab Min", "RUL_InternalIncentiveScheme", "slab_min"),
            _mapping("Slab Max", "RUL_InternalIncentiveScheme", "slab_max"),
            _mapping("Effective From", "RUL_InternalIncentiveScheme", "effective_from"),
            _mapping("Effective To", "RUL_InternalIncentiveScheme", "effective_to"),
            _mapping("Campaign Name", "RUL_InternalIncentiveScheme", "campaign_name"),
            _mapping("Notes", "RUL_InternalIncentiveScheme", "notes"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_Expense_Payment_Tracker.xlsx",
        "sheet_name": "Payments",
        "header_row": 1,
        "file_pattern": r".*Expense_Payment_Tracker.*\\.xlsx",
        "mappings": [
            _mapping("Vendor Name", "MST_Vendor", "vendor_name"),
            _mapping("Payment Head", "REF_ExpenseCategory", "name"),
            _mapping("Invoice Date", "TRN_Expense", "invoice_date"),
            _mapping("Gross Amount", "TRN_Expense", "gross_amount"),
            _mapping("TDS Amount", "TRN_Expense", "tds_amount"),
            _mapping("GST Amount", "TRN_Expense", "gst_amount"),
            _mapping("Net Amount", "TRN_Expense", "net_amount"),
            _mapping("Payment Date", "TRN_Expense", "payment_date"),
            _mapping("UTR Number", "TRN_Expense", "utr_number"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_Invoice_Dump.xlsx",
        "sheet_name": "Invoices",
        "header_row": 1,
        "file_pattern": r".*Invoice_Dump.*\\.xlsx",
        "mappings": [
            _mapping("Application No", "TRN_Invoice", "application_number"),
            _mapping("Lender Name", "TRN_Invoice", "lender_name"),
            _mapping("Customer Name", "TRN_Invoice", "customer_name"),
            _mapping("Date", "TRN_Invoice", "invoice_date"),
            _mapping("Disbursement Amount", "TRN_Invoice", "disbursement_amount"),
            _mapping("Payout Amount", "TRN_Invoice", "payout_amount"),
        ],
    },
    {
        "template_name": "MIS_TEMPLATE_Bank_Statement.xlsx",
        "sheet_name": "Transactions",
        "header_row": 1,
        "file_pattern": r".*Bank_Statement.*\\.xlsx",
        "mappings": [
            _mapping("Bank Name", "TRN_BankStatementLine", "bank_name"),
            _mapping("Transaction Date", "TRN_BankStatementLine", "transaction_date"),
            _mapping("UTR Number", "TRN_BankStatementLine", "utr_number"),
            _mapping("Amount", "TRN_BankStatementLine", "amount"),
        ],
    },
]


def seed_fixed_templates(db: Session) -> None:
    for spec in FIXED_TEMPLATE_SPECS:
        template = db.query(META_ImportTemplate).filter(META_ImportTemplate.template_name == spec["template_name"]).first()

        if template is None:
            template = META_ImportTemplate(
                template_name=spec["template_name"],
                file_pattern=spec["file_pattern"],
                fingerprint=None,
                sheet_name=spec["sheet_name"],
                header_row=spec["header_row"],
                version=1,
                status="Active",
                conflict_resolution="UPDATE",
                company_id=None,
                shared=True,
                is_active=True,
                created_by="system",
                updated_by="system",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(template)
            db.flush()

        mappings = list(spec["mappings"])
        if spec["template_name"] == "MIS_TEMPLATE_UnsecuredTracker.xlsx":
            secured = next(x for x in FIXED_TEMPLATE_SPECS if x["template_name"] == "MIS_TEMPLATE_SecuredTracker.xlsx")
            mappings = list(secured["mappings"])

        template.file_pattern = spec["file_pattern"]
        template.sheet_name = spec["sheet_name"]
        template.header_row = spec["header_row"]
        template.status = "Active"
        template.company_id = None
        template.shared = True
        template.is_active = True
        template.conflict_resolution = "UPDATE"
        template.updated_by = "system"
        template.updated_at = datetime.utcnow()
        template.mapping_definition = json.dumps(
            {
                "sheet_name": spec["sheet_name"],
                "header_row": spec["header_row"],
                "mappings": mappings,
                "conflict_resolution": "UPDATE",
            }
        )

        db.query(META_FieldMapping).filter(META_FieldMapping.template_id == template.template_id).delete()
        for mapping in mappings:
            db.add(
                META_FieldMapping(
                    template_id=template.template_id,
                    source_column=mapping["source_column"],
                    target_table=mapping["target_table"],
                    target_field=mapping["target_field"],
                    confidence_score=mapping["confidence_score"],
                    is_verified=True,
                    is_natural_key=mapping["is_natural_key"],
                    transformation_rule=None,
                    notes=mapping["notes"],
                )
            )

    db.commit()
