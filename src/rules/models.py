from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String, Text

from src.core.database import Base


class RUL_ValidationRule(Base):
    __tablename__ = "rul_validation_rule"

    rule_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    rule_code = Column(String(100), nullable=False, unique=True, index=True)
    rule_name = Column(String(255), nullable=False)
    table_name = Column(String(100), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    rule_type = Column(String(50), nullable=False, default="EXPRESSION")
    rule_expression = Column(Text, nullable=False)
    severity = Column(String(20), nullable=False, default="ERROR")
    error_message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RUL_CommissionRule(Base):
    __tablename__ = "rul_commission_rule"

    commission_rule_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    rule_code = Column(String(100), nullable=False, unique=True, index=True)
    rule_name = Column(String(255), nullable=False)
    lender_id = Column(Integer, nullable=True, index=True)
    product_id = Column(Integer, nullable=True, index=True)
    slab_type = Column(String(50), nullable=True)
    basis_type = Column(String(50), nullable=True)
    calculation_type = Column(String(50), nullable=False, default="PERCENTAGE")
    flat_rate = Column(Float, nullable=True)
    base_rate = Column(Float, nullable=True)
    base_percent = Column(Float, nullable=True)
    headline_percent = Column(Float, nullable=True)
    connector_share_percent = Column(Float, nullable=True)
    connector_share = Column(Float, nullable=True)
    effective_rate = Column(Float, nullable=True)
    pf_percent = Column(Float, nullable=True)
    i_percent = Column(Float, nullable=True)
    qualifying_condition = Column(Text, nullable=True)
    qualifying_notes = Column(Text, nullable=True)
    commercial_terms = Column(Text, nullable=True)
    clawback_conditions = Column(Text, nullable=True)
    clawback_period_months = Column(Integer, nullable=True)
    clawback_percent = Column(Float, nullable=True)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    status = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RUL_Contest(Base):
    __tablename__ = "rul_contest"

    contest_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    contest_code = Column(String(100), nullable=False, unique=True, index=True)
    contest_name = Column(String(255), nullable=False)
    frequency = Column(String(50), nullable=True)
    target_amount = Column(Float, nullable=True)
    bonus_percent = Column(Float, nullable=True)
    period = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RUL_GSTRule(Base):
    __tablename__ = "rul_gst_rule"

    gst_rule_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    rule_code = Column(String(100), nullable=False, unique=True, index=True)
    rule_name = Column(String(255), nullable=False)
    rate = Column(Float, nullable=False, default=0.0)
    applicability = Column(String(100), nullable=True)
    reverse_charge = Column(Boolean, default=False)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RUL_TDSRule(Base):
    __tablename__ = "rul_tds_rule"

    tds_rule_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    rule_code = Column(String(100), nullable=False, unique=True, index=True)
    rule_name = Column(String(255), nullable=False)
    section = Column(String(50), nullable=True)
    rate = Column(Float, nullable=False, default=0.0)
    threshold = Column(Float, nullable=True)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class RUL_InternalIncentiveScheme(Base):
    __tablename__ = "rul_internal_incentive_scheme"

    incentive_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True, default=1)
    employee_id = Column(Integer, nullable=True, index=True)
    type = Column(String(50), nullable=True)
    basis = Column(String(50), nullable=True)
    rate = Column(Float, nullable=True)
    slab_min = Column(Float, nullable=True)
    slab_max = Column(Float, nullable=True)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    campaign_name = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
