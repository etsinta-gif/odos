# src/ai/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from src.core.database import Base

class AI_Metadata(Base):
    __tablename__ = "ai_metadata"
    metadata_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("mst_company.company_id"), nullable=False)
    source_system = Column(String(100), nullable=True)
    file_name = Column(String(255), nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True)   # SHA-256
    sheet_name = Column(String(100), nullable=True)
    header_columns = Column(Text, nullable=True)                  # JSON list
    data_types = Column(Text, nullable=True)                      # JSON dict
    row_count = Column(Integer, nullable=True)
    import_batch_guid = Column(String(36), nullable=True)
    confidence = Column(Float, nullable=True)                     # overall confidence
    created_at = Column(DateTime(timezone=True), server_default=func.now())
