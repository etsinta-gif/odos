from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text

from src.core.database import Base


class BI_ReportDefinition(Base):
    __tablename__ = "bi_report_definition"

    report_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False, default="Custom")
    definition = Column(JSON, nullable=False, default=dict)

    output_format = Column(String(20), nullable=False, default="HTML")

    is_scheduled = Column(Boolean, nullable=False, default=False)
    schedule_config = Column(JSON, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    is_public = Column(Boolean, nullable=False, default=False)

    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BI_ReportExecution(Base):
    __tablename__ = "bi_report_execution"

    execution_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    triggered_by = Column(Integer, nullable=True, index=True)
    triggered_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    output_url = Column(String(500), nullable=True)
    output_size = Column(Integer, nullable=True)

    status = Column(String(20), nullable=False, default="PENDING", index=True)
    error_message = Column(Text, nullable=True)

    row_count = Column(Integer, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)


class BI_ReportSchedule(Base):
    __tablename__ = "bi_report_schedule"

    schedule_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    frequency = Column(String(20), nullable=False, default="DAILY")
    day_of_week = Column(String(10), nullable=True)
    day_of_month = Column(Integer, nullable=True)
    run_time = Column(String(5), nullable=False, default="09:00")
    recipients = Column(JSON, nullable=True)

    next_run_at = Column(DateTime, nullable=True, index=True)
    last_run_at = Column(DateTime, nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BI_DashboardDefinition(Base):
    __tablename__ = "bi_dashboard_definition"

    dashboard_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    layout = Column(JSON, nullable=False, default=dict)

    is_active = Column(Boolean, nullable=False, default=True)
    is_default = Column(Boolean, nullable=False, default=False)

    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BI_WidgetDefinition(Base):
    __tablename__ = "bi_widget_definition"

    widget_id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(Integer, nullable=False, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    title = Column(String(255), nullable=False)
    type = Column(String(20), nullable=False)
    chart_type = Column(String(20), nullable=True)

    report_id = Column(Integer, nullable=True, index=True)
    query_definition = Column(JSON, nullable=True)

    position_x = Column(Integer, nullable=False, default=0)
    position_y = Column(Integer, nullable=False, default=0)
    width = Column(Integer, nullable=False, default=4)
    height = Column(Integer, nullable=False, default=3)

    is_active = Column(Boolean, nullable=False, default=True)

    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
