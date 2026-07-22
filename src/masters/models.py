from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, JSON, Numeric, String, Text, UniqueConstraint

from src.core.database import Base


class MST_Party(Base):
    __tablename__ = "mst_party"
    __table_args__ = (
        UniqueConstraint("company_id", "pan", name="uq_mst_party_company_pan"),
    )

    party_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)

    # Core identity
    name = Column(String(255), nullable=False)
    pan = Column(String(20), nullable=False, index=True)
    gstin = Column(String(30), nullable=True)
    classification = Column(String(50), nullable=False, default="Unknown")

    # Cross-verification defaults
    default_gst_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    default_tds_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    max_commission = Column(Numeric(15, 2), nullable=True)

    # Source-specific flexibility
    metadata_json = Column("metadata", JSON, nullable=False, default=dict)

    # Status and audit
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True, index=True)
    updated_by = Column(Integer, nullable=True, index=True)


class MST_Customer(Base):
    __tablename__ = "mst_customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    full_name = Column(String(255), nullable=False)
    pan = Column(String(20), nullable=False, unique=True, index=True)
    gstin = Column(String(30), nullable=True)
    email = Column(String(255), nullable=True)
    mobile = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    occupation = Column(String(100), nullable=True)
    annual_income = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_Lender(Base):
    __tablename__ = "mst_lender"

    lender_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    lender_name = Column(String(255), nullable=False)
    pan = Column(String(20), nullable=False, unique=True, index=True)
    gstin = Column(String(30), nullable=True)
    lender_code = Column(String(50), nullable=True, unique=True)
    dsa_code = Column(String(100), nullable=True)
    default_gst_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    default_tds_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    max_commission = Column(Numeric(15, 2), nullable=True)
    metadata_json = Column("metadata", JSON, nullable=False, default=dict)
    is_nbfc = Column(Boolean, default=False)
    credit_rating = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_Product(Base):
    __tablename__ = "mst_product"

    product_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    product_name = Column(String(255), nullable=False)
    product_code = Column(String(50), nullable=True, unique=True)
    lender_id = Column(Integer, nullable=True, index=True)
    category = Column(String(255), nullable=True)
    sub_product = Column(String(255), nullable=True)
    borrower_salary_range = Column(String(255), nullable=True)
    roi_percent = Column(Float, nullable=True)
    is_employed = Column(Boolean, default=False)
    interest_rate = Column(Float, nullable=True)
    min_loan_amount = Column(Float, nullable=True)
    max_loan_amount = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_Employee(Base):
    __tablename__ = "mst_employee"

    employee_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    employee_code = Column(String(50), nullable=True, unique=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    father_name = Column(String(255), nullable=True)
    marital_status = Column(String(50), nullable=True)
    pan = Column(String(20), nullable=True)
    aadhar_number = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)
    date_of_joining = Column(Date, nullable=True)
    designation = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    team_name = Column(String(100), nullable=True)
    branch_id = Column(Integer, nullable=True)
    pf_applicable = Column(Boolean, default=False)
    esic_applicable = Column(Boolean, default=False)
    email = Column(String(255), nullable=True)
    mobile = Column(String(20), nullable=True)
    bank_name = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_ifsc = Column(String(20), nullable=True)
    uan_number = Column(String(30), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_Connector(Base):
    __tablename__ = "mst_connector"

    connector_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    connector_code = Column(String(50), nullable=True, unique=True)
    connector_name = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    pan = Column(String(20), nullable=True)
    gstin = Column(String(30), nullable=True)
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc = Column(String(20), nullable=True)
    default_gst_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    default_tds_rate = Column(Numeric(5, 2), nullable=False, default=0.0)
    max_commission = Column(Numeric(15, 2), nullable=True)
    metadata_json = Column("metadata", JSON, nullable=False, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_DSA(Base):
    __tablename__ = "mst_dsa"

    dsa_id = Column(Integer, primary_key=True, index=True)
    dsa_code = Column(String(50), nullable=False, unique=True, index=True)
    dsa_name = Column(String(255), nullable=False)
    contact_person = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    mobile = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_ConnectorBank(Base):
    __tablename__ = "mst_connector_bank"

    connector_bank_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    connector_id = Column(Integer, nullable=True, index=True)
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_EmployeeBankAccount(Base):
    __tablename__ = "mst_employee_bank_account"

    employee_bank_account_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    employee_id = Column(Integer, nullable=True, index=True)
    bank_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc_code = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MST_Vendor(Base):
    __tablename__ = "mst_vendor"

    vendor_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    vendor_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)


class MST_ExpenseCategory(Base):
    __tablename__ = "mst_expense_category"

    expense_category_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    category_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)


class MST_CostCenter(Base):
    __tablename__ = "mst_cost_center"

    cost_center_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    center_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)


class MST_CompanyBankAccount(Base):
    __tablename__ = "mst_company_bank_account"

    bank_account_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    bank_name = Column(String(255), nullable=False)
    account_number = Column(String(50), nullable=True)
    ifsc = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)