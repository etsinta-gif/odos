from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text

from src.core.database import Base


class ALERT_Rule(Base):
    __tablename__ = "alert_rules"

    rule_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), nullable=False)

    conditions = Column(JSON, nullable=False, default=dict)
    actions = Column(JSON, nullable=False, default=list)

    escalation_policy_id = Column(Integer, nullable=True, index=True)

    is_active = Column(Boolean, nullable=False, default=True)
    priority = Column(Integer, nullable=False, default=1)

    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ALERT_EscalationPolicy(Base):
    __tablename__ = "alert_escalation_policies"

    policy_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    levels = Column(JSON, nullable=False, default=list)
    default_assignee_role = Column(String(50), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    created_by = Column(Integer, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_by = Column(Integer, nullable=True, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ALERT_Notification(Base):
    __tablename__ = "alert_notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    rule_id = Column(Integer, nullable=True, index=True)
    red_flag_id = Column(Integer, nullable=True, index=True)

    type = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    payload = Column(JSON, nullable=True)

    recipient_user_id = Column(Integer, nullable=True, index=True)
    recipient_email = Column(String(255), nullable=True, index=True)

    sent_at = Column(DateTime, default=datetime.utcnow, index=True)
    delivered = Column(Boolean, nullable=False, default=True)
    error_message = Column(Text, nullable=True)

    is_read = Column(Boolean, nullable=False, default=False, index=True)
    read_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class ALERT_AuditLog(Base):
    __tablename__ = "alert_audit_logs"

    log_id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)

    red_flag_id = Column(Integer, nullable=True, index=True)
    rule_id = Column(Integer, nullable=True, index=True)

    action = Column(String(50), nullable=False, index=True)
    details = Column(JSON, nullable=True)

    performed_by = Column(Integer, nullable=True, index=True)
    performed_at = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String(45), nullable=True)
