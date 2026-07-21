"""IMP-5B tenant rollout: add company_id to operational tables

Revision ID: 0005_imp_5b
Revises: 0004_imp_5b
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0005_imp_5b"
down_revision = "0004_imp_5b"
branch_labels = None
depends_on = None


TABLES = [
    "mst_customer",
    "mst_lender",
    "mst_product",
    "mst_employee",
    "mst_connector",
    "mst_connector_bank",
    "mst_employee_bank_account",
    "mst_vendor",
    "mst_expense_category",
    "mst_cost_center",
    "mst_company_bank_account",
    "trn_case",
    "trn_case_status_history",
    "trn_tally_export_batch",
    "trn_tally_export_detail",
    "trn_revenue",
    "trn_commission",
    "trn_expense",
    "trn_payment",
    "trn_recurring_expense",
    "trn_expense_claim",
    "trn_invoice",
    "trn_case_connector_split",
    "trn_incentive_earned",
    "rul_validation_rule",
    "rul_commission_rule",
    "rul_contest",
    "rul_gst_rule",
    "rul_tds_rule",
    "rul_internal_incentive_scheme",
]


def _has_table(inspector, table_name):
    return table_name in inspector.get_table_names()


def _has_column(inspector, table_name, column_name):
    if not _has_table(inspector, table_name):
        return False
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def _has_index(inspector, table_name, index_name):
    if not _has_table(inspector, table_name):
        return False
    return any(idx["name"] == index_name for idx in inspector.get_indexes(table_name))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name in TABLES:
        if not _has_table(inspector, table_name):
            continue
        if not _has_column(inspector, table_name, "company_id"):
            op.add_column(
                table_name,
                sa.Column("company_id", sa.Integer(), nullable=False, server_default="1"),
            )
        index_name = f"ix_{table_name}_company_id"
        if not _has_index(inspector, table_name, index_name):
            op.create_index(index_name, table_name, ["company_id"], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name in TABLES:
        if not _has_table(inspector, table_name):
            continue
        index_name = f"ix_{table_name}_company_id"
        if _has_index(inspector, table_name, index_name):
            op.drop_index(index_name, table_name=table_name)
        if _has_column(inspector, table_name, "company_id"):
            op.drop_column(table_name, "company_id")
