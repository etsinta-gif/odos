from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String, Text, UniqueConstraint

from src.core.database import Base


class TRN_Case(Base):
    __tablename__ = "trn_case"

    case_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_number = Column(String(100), nullable=False, unique=True, index=True)
    customer_id = Column(Integer, nullable=False, index=True)
    customer_name = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    lender_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    region_id = Column(Integer, nullable=True, index=True)
    unit_head_id = Column(Integer, nullable=True, index=True)
    sales_manager_id = Column(Integer, nullable=True, index=True)
    application_date = Column(Date, nullable=True)
    sanction_date = Column(Date, nullable=True)
    disbursement_date = Column(Date, nullable=True)
    confirmed_by_bank_date = Column(Date, nullable=True)
    branch_code = Column(String(100), nullable=True)
    branch_name = Column(String(255), nullable=True)
    referral_source = Column(String(255), nullable=True)
    sanction_amount = Column(Float, nullable=True)
    disbursement_amount = Column(Float, nullable=True)
    total_disbursement_amount = Column(Float, nullable=True)
    remarks = Column(Text, nullable=True)
    is_cancelled = Column(Boolean, default=False)
    status = Column(String(100), default="LEAD")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_CaseStatusHistory(Base):
    __tablename__ = "trn_case_status_history"

    history_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=False, index=True)
    status = Column(String(100), nullable=False)
    changed_at = Column(DateTime, default=datetime.utcnow)


class TRN_TallyExportBatch(Base):
    __tablename__ = "trn_tally_export_batch"

    batch_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    batch_number = Column(String(100), unique=True, index=True)
    batch_name = Column(String(255), nullable=False)
    export_type = Column(String(50), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    total_records = Column(Integer, default=0)
    exported_records = Column(Integer, default=0)
    export_status = Column(String(50), default="PENDING")
    sync_status = Column(String(50), default="PENDING")
    file_path = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_TallyExportDetail(Base):
    __tablename__ = "trn_tally_export_detail"

    detail_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    batch_id = Column(Integer, nullable=False, index=True)
    source_table = Column(String(100), nullable=False)
    source_id = Column(Integer, nullable=False)
    exported_data = Column(Text, nullable=True)
    export_status = Column(String(50), default="PENDING")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TRN_Revenue(Base):
    __tablename__ = "trn_revenue"

    revenue_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=True, index=True)
    revenue_date = Column(Date, nullable=False)
    rate_percent = Column(Float, nullable=True)
    gross_amount = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    base_revenue_amount = Column(Float, nullable=True)
    gst_amount = Column(Float, default=0.0)
    tds_amount = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    utr_number = Column(String(255), nullable=True, unique=True)
    payment_status = Column(String(50), default="PENDING")
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_Commission(Base):
    __tablename__ = "trn_commission"

    commission_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=True, index=True)
    connector_id = Column(Integer, nullable=True, index=True)
    commission_date = Column(Date, nullable=False)
    rate_percent = Column(Float, nullable=True)
    gross_amount = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    base_commission_amount = Column(Float, nullable=True)
    bonus_commission_amount = Column(Float, default=0.0)
    gross_commission_amount = Column(Float, nullable=True)
    gst_amount = Column(Float, default=0.0)
    tds_amount = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    payment_request_date = Column(Date, nullable=True)
    payment_paid_date = Column(Date, nullable=True)
    utr_number = Column(String(255), nullable=True)
    advance_paid = Column(Float, nullable=True)
    advance_date = Column(Date, nullable=True)
    recovery_made = Column(Float, nullable=True)
    recovery_date = Column(Date, nullable=True)
    payment_status = Column(String(50), default="PENDING")
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_Expense(Base):
    __tablename__ = "trn_expense"

    expense_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    expense_date = Column(Date, nullable=False)
    vendor_id = Column(Integer, nullable=True, index=True)
    expense_category_id = Column(Integer, nullable=True, index=True)
    cost_center_id = Column(Integer, nullable=True, index=True)
    case_id = Column(Integer, nullable=True, index=True)
    invoice_date = Column(Date, nullable=True)
    payment_date = Column(Date, nullable=True)
    utr_number = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    gross_amount = Column(Float, nullable=True)
    amount = Column(Float, nullable=False)
    gst_amount = Column(Float, default=0.0)
    tds_amount = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    payment_status = Column(String(50), default="PENDING")
    invoice_reference = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_Payment(Base):
    __tablename__ = "trn_payment"

    payment_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    payment_number = Column(String(100), nullable=True, unique=True, index=True)
    payment_date = Column(Date, nullable=False)
    company_bank_account_id = Column(Integer, nullable=True, index=True)
    payment_amount = Column(Float, nullable=False)
    payment_mode = Column(String(100), nullable=False)
    utr_number = Column(String(255), nullable=True, unique=True)
    payment_type = Column(String(100), nullable=False)
    reference_id = Column(Integer, nullable=True, index=True)
    reconciliation_status = Column(String(50), default="PENDING")
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_RecurringExpense(Base):
    __tablename__ = "trn_recurring_expense"

    recurring_expense_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    expense_category_id = Column(Integer, nullable=False, index=True)
    vendor_id = Column(Integer, nullable=True, index=True)
    cost_center_id = Column(Integer, nullable=True, index=True)
    description = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    gst_amount = Column(Float, default=0.0)
    tds_amount = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    frequency = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    invoice_reference = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_ExpenseClaim(Base):
    __tablename__ = "trn_expense_claim"

    expense_claim_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    employee_id = Column(Integer, nullable=True, index=True)
    amount = Column(Float, nullable=True)
    status = Column(String(50), default="PENDING")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_Invoice(Base):
    __tablename__ = "trn_invoice"

    invoice_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=True, index=True)
    invoice_number = Column(String(100), nullable=True, index=True)
    application_number = Column(String(100), nullable=True, index=True)
    lender_name = Column(String(255), nullable=True)
    customer_name = Column(String(255), nullable=True)
    invoice_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    received_date = Column(Date, nullable=True)
    utr_number = Column(String(255), nullable=True)
    disbursement_amount = Column(Float, nullable=True)
    payout_amount = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_CaseConnectorSplit(Base):
    __tablename__ = "trn_case_connector_split"

    split_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=False, index=True)
    connector_id = Column(Integer, nullable=True, index=True)
    share_percent = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_IncentiveEarned(Base):
    __tablename__ = "trn_incentive_earned"

    incentive_earned_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    case_id = Column(Integer, nullable=True, index=True)
    employee_id = Column(Integer, nullable=True, index=True)
    incentive_percent = Column(Float, nullable=True)
    amount = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_Salary(Base):
    __tablename__ = "trn_salary"

    salary_id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=True, index=True)
    pay_month = Column(Date, nullable=True)
    basic_da = Column(Float, nullable=True)
    hra = Column(Float, nullable=True)
    other_allowance = Column(Float, nullable=True)
    gross_earnings = Column(Float, nullable=True)
    commission_amount = Column(Float, nullable=True)
    include_commission_in_tax = Column(Boolean, default=False)
    total_earnings = Column(Float, nullable=True)
    advance_salary = Column(Float, nullable=True)
    net_payable = Column(Float, nullable=True)
    utr_number = Column(String(255), nullable=True)
    payment_date = Column(Date, nullable=True)
    tagged_employee_id = Column(Integer, nullable=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_StatutoryPayment(Base):
    __tablename__ = "trn_statutory_payment"

    statutory_payment_id = Column(Integer, primary_key=True, index=True)
    salary_id = Column(Integer, nullable=True, index=True)
    pf_employee_share = Column(Float, nullable=True)
    pf_employer_share = Column(Float, nullable=True)
    esic_employee_share = Column(Float, nullable=True)
    esic_employer_share = Column(Float, nullable=True)
    professional_tax = Column(Float, nullable=True)
    tds_amount = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TRN_BankStatementLine(Base):
    __tablename__ = "trn_bank_statement_line"

    statement_line_id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String(255), nullable=False)
    transaction_date = Column(Date, nullable=True)
    utr_number = Column(String(255), nullable=True, index=True)
    amount = Column(Float, nullable=True)
    is_reconciled = Column(Boolean, default=False)
    reconciled_to = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ETL_ImportBatch(Base):
    __tablename__ = "etl_import_batch"

    batch_id = Column(Integer, primary_key=True, index=True)
    batch_guid = Column(String(64), nullable=False, unique=True, index=True)
    template_id = Column(Integer, nullable=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    source_system = Column(String(100), nullable=False, default="FCPL")
    file_name = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=True, index=True)
    import_status = Column(String(50), nullable=False, default="STAGED")
    is_atomic_transaction = Column(Boolean, default=False)
    is_complete = Column(Boolean, default=False)
    import_datetime = Column(DateTime, default=datetime.utcnow)
    total_rows = Column(Integer, default=0)
    successful_rows = Column(Integer, default=0)
    failed_rows = Column(Integer, default=0)


class ETL_StagingRawData(Base):
    __tablename__ = "etl_staging_raw_data"

    staging_id = Column(Integer, primary_key=True, index=True)
    batch_guid = Column(String(64), nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    table_name = Column(String(100), nullable=False, index=True)
    column_name = Column(String(100), nullable=True)
    source_row_number = Column(Integer, nullable=True)
    source_column_name = Column(String(100), nullable=True)
    source_value = Column(Text, nullable=True)
    target_field = Column(String(100), nullable=True)
    stored_value = Column(Text, nullable=True)
    validation_status = Column(String(50), nullable=False, default="PENDING")
    is_promoted = Column(Boolean, default=False)
    import_datetime = Column(DateTime, default=datetime.utcnow)


class ETL_ErrorLog(Base):
    __tablename__ = "etl_error_log"

    error_id = Column(Integer, primary_key=True, index=True)
    batch_guid = Column(String(64), nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    table_name = Column(String(100), nullable=True)
    row_number = Column(Integer, nullable=True)
    column_name = Column(String(100), nullable=True)
    error_type = Column(String(50), nullable=False, default="VALIDATION")
    error_message = Column(Text, nullable=False)
    error_datetime = Column(DateTime, default=datetime.utcnow)


class ETL_DataLineage(Base):
    __tablename__ = "etl_data_lineage"

    lineage_id = Column(Integer, primary_key=True, index=True)
    batch_guid = Column(String(64), nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    staging_id = Column(Integer, nullable=True, index=True)
    target_table = Column(String(100), nullable=False)
    target_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class RUL_CommissionSlab(Base):
    __tablename__ = "rul_commission_slab"
    __table_args__ = (
        UniqueConstraint("commission_rule_id", "tier_name", name="uq_rul_commission_slab_rule_tier"),
    )

    slab_id = Column(Integer, primary_key=True, index=True)
    commission_rule_id = Column(Integer, nullable=True, index=True)
    slab_label = Column(String(100), nullable=False, index=True)
    tier_name = Column(String(100), nullable=True)
    tier_min = Column(Float, nullable=True)
    tier_max = Column(Float, nullable=True)
    rate = Column(Float, nullable=False, default=0.0)
    connector_share = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
