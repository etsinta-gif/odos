from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.core.database import Base


class _ReferenceBase:
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(100), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class REF_LoanType(_ReferenceBase, Base):
    __tablename__ = "ref_loan_type"


class REF_Channel(_ReferenceBase, Base):
    __tablename__ = "ref_channel"


class REF_ProductCategory(_ReferenceBase, Base):
    __tablename__ = "ref_product_category"


class REF_Status(_ReferenceBase, Base):
    __tablename__ = "ref_status"


class REF_Region(_ReferenceBase, Base):
    __tablename__ = "ref_region"


class REF_BorrowerProfile(_ReferenceBase, Base):
    __tablename__ = "ref_borrower_profile"


class REF_LoanNature(_ReferenceBase, Base):
    __tablename__ = "ref_loan_nature"


class REF_Location(_ReferenceBase, Base):
    __tablename__ = "ref_location"


class REF_ExpenseCategory(_ReferenceBase, Base):
    __tablename__ = "ref_expense_category"