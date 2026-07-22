"""IMP-INTEL-2 BI layer schema

Revision ID: 0008_imp_intel_2
Revises: 0007_imp_intel_1
Create Date: 2026-07-22
"""

from alembic import op
import sqlalchemy as sa


revision = "0008_imp_intel_2"
down_revision = "0007_imp_intel_1"
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

    if not _has_table(inspector, "bi_report_definition"):
        op.create_table(
            "bi_report_definition",
            sa.Column("report_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("category", sa.String(length=50), nullable=False, server_default="Custom"),
            sa.Column("definition", sa.JSON(), nullable=False),
            sa.Column("output_format", sa.String(length=20), nullable=False, server_default="HTML"),
            sa.Column("is_scheduled", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("schedule_config", sa.JSON(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("is_public", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "bi_report_execution"):
        op.create_table(
            "bi_report_execution",
            sa.Column("execution_id", sa.Integer(), primary_key=True),
            sa.Column("report_id", sa.Integer(), nullable=False),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("triggered_by", sa.Integer(), nullable=True),
            sa.Column("triggered_at", sa.DateTime(), nullable=True),
            sa.Column("completed_at", sa.DateTime(), nullable=True),
            sa.Column("output_url", sa.String(length=500), nullable=True),
            sa.Column("output_size", sa.Integer(), nullable=True),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="PENDING"),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("row_count", sa.Integer(), nullable=True),
            sa.Column("execution_time_ms", sa.Integer(), nullable=True),
        )

    if not _has_table(inspector, "bi_report_schedule"):
        op.create_table(
            "bi_report_schedule",
            sa.Column("schedule_id", sa.Integer(), primary_key=True),
            sa.Column("report_id", sa.Integer(), nullable=False),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("frequency", sa.String(length=20), nullable=False, server_default="DAILY"),
            sa.Column("day_of_week", sa.String(length=10), nullable=True),
            sa.Column("day_of_month", sa.Integer(), nullable=True),
            sa.Column("run_time", sa.String(length=5), nullable=False, server_default="09:00"),
            sa.Column("recipients", sa.JSON(), nullable=True),
            sa.Column("next_run_at", sa.DateTime(), nullable=True),
            sa.Column("last_run_at", sa.DateTime(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "bi_dashboard_definition"):
        op.create_table(
            "bi_dashboard_definition",
            sa.Column("dashboard_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("layout", sa.JSON(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    if not _has_table(inspector, "bi_widget_definition"):
        op.create_table(
            "bi_widget_definition",
            sa.Column("widget_id", sa.Integer(), primary_key=True),
            sa.Column("dashboard_id", sa.Integer(), nullable=False),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("type", sa.String(length=20), nullable=False),
            sa.Column("chart_type", sa.String(length=20), nullable=True),
            sa.Column("report_id", sa.Integer(), nullable=True),
            sa.Column("query_definition", sa.JSON(), nullable=True),
            sa.Column("position_x", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("position_y", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("width", sa.Integer(), nullable=False, server_default="4"),
            sa.Column("height", sa.Integer(), nullable=False, server_default="3"),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )

    _create_index_if_missing(inspector, "bi_report_definition", "ix_bi_report_definition_report_id", ["report_id"])
    _create_index_if_missing(inspector, "bi_report_definition", "ix_bi_report_definition_company_id", ["company_id"])
    _create_index_if_missing(inspector, "bi_report_definition", "ix_bi_report_definition_created_by", ["created_by"])

    _create_index_if_missing(inspector, "bi_report_execution", "ix_bi_report_execution_execution_id", ["execution_id"])
    _create_index_if_missing(inspector, "bi_report_execution", "ix_bi_report_execution_report_id", ["report_id"])
    _create_index_if_missing(inspector, "bi_report_execution", "ix_bi_report_execution_company_id", ["company_id"])
    _create_index_if_missing(inspector, "bi_report_execution", "ix_bi_report_execution_status", ["status"])

    _create_index_if_missing(inspector, "bi_report_schedule", "ix_bi_report_schedule_schedule_id", ["schedule_id"])
    _create_index_if_missing(inspector, "bi_report_schedule", "ix_bi_report_schedule_report_id", ["report_id"])
    _create_index_if_missing(inspector, "bi_report_schedule", "ix_bi_report_schedule_company_id", ["company_id"])
    _create_index_if_missing(inspector, "bi_report_schedule", "ix_bi_report_schedule_next_run_at", ["next_run_at"])

    _create_index_if_missing(inspector, "bi_dashboard_definition", "ix_bi_dashboard_definition_dashboard_id", ["dashboard_id"])
    _create_index_if_missing(inspector, "bi_dashboard_definition", "ix_bi_dashboard_definition_company_id", ["company_id"])

    _create_index_if_missing(inspector, "bi_widget_definition", "ix_bi_widget_definition_widget_id", ["widget_id"])
    _create_index_if_missing(inspector, "bi_widget_definition", "ix_bi_widget_definition_dashboard_id", ["dashboard_id"])
    _create_index_if_missing(inspector, "bi_widget_definition", "ix_bi_widget_definition_company_id", ["company_id"])
    _create_index_if_missing(inspector, "bi_widget_definition", "ix_bi_widget_definition_report_id", ["report_id"])


def downgrade():
    op.drop_table("bi_widget_definition")
    op.drop_table("bi_dashboard_definition")
    op.drop_table("bi_report_schedule")
    op.drop_table("bi_report_execution")
    op.drop_table("bi_report_definition")
