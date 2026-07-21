from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

from src.core.database import Base


class AI_Metadata(Base):
    __tablename__ = "ai_metadata"

    metadata_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=True, index=True, default=1)
    source_system = Column(String(100), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True, index=True)
    sheet_name = Column(String(100), nullable=True)
    header_columns = Column(Text, nullable=True)
    data_types = Column(Text, nullable=True)
    row_count = Column(Integer, nullable=True)
    import_batch_guid = Column(String(64), nullable=True, index=True)
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AI_Mapping(Base):
    __tablename__ = "ai_mapping"

    mapping_id = Column(Integer, primary_key=True, index=True)
    metadata_id = Column(Integer, nullable=True, index=True)
    source_column = Column(String(255), nullable=False)
    target_table = Column(String(100), nullable=False)
    target_field = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=True)
    is_verified = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AI_Learning(Base):
    __tablename__ = "ai_learning"

    learning_id = Column(Integer, primary_key=True, index=True)
    metadata_id = Column(Integer, nullable=True, index=True)
    mapping_id = Column(Integer, nullable=True, index=True)
    event_type = Column(String(100), nullable=False)
    event_payload = Column(Text, nullable=True)
    model_name = Column(String(255), nullable=True)
    model_version = Column(String(100), nullable=True)
    confidence_before = Column(Float, nullable=True)
    confidence_after = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class AI_Feedback(Base):
    __tablename__ = "ai_feedback"

    feedback_id = Column(Integer, primary_key=True, index=True)
    metadata_id = Column(Integer, nullable=True, index=True)
    template_id = Column(Integer, nullable=True, index=True)
    batch_guid = Column(String(64), nullable=True, index=True)
    sheet_name = Column(String(255), nullable=True)
    source_column = Column(String(255), nullable=True)
    target_table = Column(String(100), nullable=True)
    target_field = Column(String(100), nullable=True)
    confidence_score = Column(Integer, nullable=True)
    confidence_level = Column(String(20), nullable=True)
    formula_detected = Column(Boolean, default=False)
    formula_status = Column(String(50), nullable=True)
    user_decision = Column(String(50), nullable=False, default="APPROVED")
    discrepancy_reason = Column(Text, nullable=True)
    feedback_payload = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
