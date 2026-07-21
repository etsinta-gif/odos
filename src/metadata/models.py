from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.core.database import Base


class META_ImportTemplate(Base):
    __tablename__ = "meta_import_template"

    template_id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(255), nullable=False)
    file_pattern = Column(String(255), nullable=True)
    fingerprint = Column(String(128), nullable=True, index=True)
    sheet_name = Column(String(255), nullable=False, default="Sheet1")
    header_row = Column(Integer, nullable=False, default=1)
    mapping_definition = Column(Text, nullable=True)
    mapping_definition_history = Column(Text, nullable=True)
    version = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="Draft")
    conflict_resolution = Column(String(20), nullable=False, default="SKIP")
    company_id = Column(Integer, nullable=True, index=True)
    shared = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(String(100), nullable=True, default="admin")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_by = Column(String(100), nullable=True, default="admin")
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    mappings = relationship("META_FieldMapping", back_populates="template", cascade="all, delete-orphan")


class META_FieldMapping(Base):
    __tablename__ = "meta_field_mapping"

    mapping_id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("meta_import_template.template_id"), nullable=False, index=True)
    company_id = Column(Integer, nullable=True, index=True)
    source_column = Column(String(255), nullable=False)
    target_table = Column(String(100), nullable=False)
    target_field = Column(String(100), nullable=False)
    confidence_score = Column(Integer, nullable=False, default=0)
    is_verified = Column(Boolean, nullable=False, default=False)
    is_natural_key = Column(Boolean, nullable=False, default=False)
    transformation_rule = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)

    template = relationship("META_ImportTemplate", back_populates="mappings")
