"""IMP-INTEL-3 automation alerts and notifications schema

Revision ID: 0009_imp_intel_3
Revises: 0008_imp_intel_2
Create Date: 2026-07-22
"""

from alembic import op
import sqlalchemy as sa


revision = "0009_imp_intel_3"
down_revision = "0008_imp_intel_2"
branch_labels = None
depends_on = None


def _has_table(inspector, table_name):
    return table_name in inspector.get_table_names()


def _has_index(inspector, table_name, index_name):
    if not _has_table(inspector, table_name):
        return False
    return any(idx["name"] == index_name for idx in inspector.get_indexes(table_name))


def _create_index_if_missing(inspector, table_name, index_name, columns):
    if _has_table(inspector, table_name) and not _has_index(inspector, table_name, index_name):
        op.create_index(index_name, table_name, columns, unique=False)


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "alert_escalation_policies"):
        op.create_table(
            "alert_escalation_policies",
            sa.Column("policy_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("levels", sa.JSON(), nullable=False),
            sa.Column("default_assignee_role", sa.String(length=50), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "alert_rules"):
        op.create_table(
            "alert_rules",
            sa.Column("rule_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("category", sa.String(length=50), nullable=False),
            sa.Column("conditions", sa.JSON(), nullable=False),
            sa.Column("actions", sa.JSON(), nullable=False),
            sa.Column("escalation_policy_id", sa.Integer(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("priority", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "alert_notifications"):
        op.create_table(
            "alert_notifications",
            sa.Column("notification_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("rule_id", sa.Integer(), nullable=True),
            sa.Column("red_flag_id", sa.Integer(), nullable=True),
            sa.Column("type", sa.String(length=20), nullable=False),
            sa.Column("subject", sa.String(length=255), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("payload", sa.JSON(), nullable=True),
            sa.Column("recipient_user_id", sa.Integer(), nullable=True),
            sa.Column("recipient_email", sa.String(length=255), nullable=True),
            sa.Column("sent_at", sa.DateTime(), nullable=True),
            sa.Column("delivered", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("read_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "alert_audit_logs"):
        op.create_table(
            "alert_audit_logs",
            sa.Column("log_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("red_flag_id", sa.Integer(), nullable=True),
            sa.Column("rule_id", sa.Integer(), nullable=True),
            sa.Column("action", sa.String(length=50), nullable=False),
            sa.Column("details", sa.JSON(), nullable=True),
            sa.Column("performed_by", sa.Integer(), nullable=True),
            sa.Column("performed_at", sa.DateTime(), nullable=True),
            sa.Column("ip_address", sa.String(length=45), nullable=True),
        )

    _create_index_if_missing(inspector, "alert_escalation_policies", "ix_alert_escalation_policies_policy_id", ["policy_id"])
    _create_index_if_missing(inspector, "alert_escalation_policies", "ix_alert_escalation_policies_company_id", ["company_id"])

    _create_index_if_missing(inspector, "alert_rules", "ix_alert_rules_rule_id", ["rule_id"])
    _create_index_if_missing(inspector, "alert_rules", "ix_alert_rules_company_id", ["company_id"])
    _create_index_if_missing(inspector, "alert_rules", "ix_alert_rules_escalation_policy_id", ["escalation_policy_id"])

    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_notification_id", ["notification_id"])
    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_company_id", ["company_id"])
    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_red_flag_id", ["red_flag_id"])
    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_rule_id", ["rule_id"])
    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_recipient_user_id", ["recipient_user_id"])
    _create_index_if_missing(inspector, "alert_notifications", "ix_alert_notifications_is_read", ["is_read"])

    _create_index_if_missing(inspector, "alert_audit_logs", "ix_alert_audit_logs_log_id", ["log_id"])
    _create_index_if_missing(inspector, "alert_audit_logs", "ix_alert_audit_logs_company_id", ["company_id"])
    _create_index_if_missing(inspector, "alert_audit_logs", "ix_alert_audit_logs_red_flag_id", ["red_flag_id"])
    _create_index_if_missing(inspector, "alert_audit_logs", "ix_alert_audit_logs_rule_id", ["rule_id"])
    _create_index_if_missing(inspector, "alert_audit_logs", "ix_alert_audit_logs_action", ["action"])


def downgrade():
    op.drop_table("alert_audit_logs")
    op.drop_table("alert_notifications")
    op.drop_table("alert_rules")
    op.drop_table("alert_escalation_policies")
