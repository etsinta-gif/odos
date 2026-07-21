"""IMP-5.9 governance and rules

Revision ID: 0002_imp_59
Revises: 0001_initial
Create Date: 2026-07-20
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_imp_59"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def _has_column(inspector, table_name, column_name):
    if table_name not in inspector.get_table_names():
        return False
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "meta_import_template" in inspector.get_table_names():
        if not _has_column(inspector, "meta_import_template", "mapping_definition_history"):
            op.add_column("meta_import_template", sa.Column("mapping_definition_history", sa.Text(), nullable=True))
        if not _has_column(inspector, "meta_import_template", "conflict_resolution"):
            op.add_column("meta_import_template", sa.Column("conflict_resolution", sa.String(length=20), nullable=False, server_default="SKIP"))

    if "meta_field_mapping" in inspector.get_table_names() and not _has_column(inspector, "meta_field_mapping", "is_natural_key"):
        op.add_column("meta_field_mapping", sa.Column("is_natural_key", sa.Boolean(), nullable=False, server_default=sa.false()))

    if "rul_validation_rule" not in inspector.get_table_names():
        op.create_table(
            "rul_validation_rule",
            sa.Column("rule_id", sa.Integer(), primary_key=True, index=True),
            sa.Column("rule_code", sa.String(length=100), nullable=False),
            sa.Column("rule_name", sa.String(length=255), nullable=False),
            sa.Column("table_name", sa.String(length=100), nullable=False),
            sa.Column("field_name", sa.String(length=100), nullable=False),
            sa.Column("rule_type", sa.String(length=50), nullable=False, server_default="EXPRESSION"),
            sa.Column("rule_expression", sa.Text(), nullable=False),
            sa.Column("severity", sa.String(length=20), nullable=False, server_default="ERROR"),
            sa.Column("error_message", sa.Text(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column("priority", sa.Integer(), nullable=True, server_default="100"),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.UniqueConstraint("rule_code", name="uq_rul_validation_rule_rule_code"),
        )
        op.create_index("ix_rul_validation_rule_rule_code", "rul_validation_rule", ["rule_code"])
        op.create_index("ix_rul_validation_rule_table_name", "rul_validation_rule", ["table_name"])

    if "rul_commission_rule" not in inspector.get_table_names():
        op.create_table(
            "rul_commission_rule",
            sa.Column("commission_rule_id", sa.Integer(), primary_key=True, index=True),
            sa.Column("rule_code", sa.String(length=100), nullable=False),
            sa.Column("rule_name", sa.String(length=255), nullable=False),
            sa.Column("lender_id", sa.Integer(), nullable=True),
            sa.Column("product_id", sa.Integer(), nullable=True),
            sa.Column("basis_type", sa.String(length=50), nullable=True),
            sa.Column("calculation_type", sa.String(length=50), nullable=False, server_default="PERCENTAGE"),
            sa.Column("flat_rate", sa.Float(), nullable=True),
            sa.Column("base_rate", sa.Float(), nullable=True),
            sa.Column("connector_share", sa.Float(), nullable=True),
            sa.Column("effective_rate", sa.Float(), nullable=True),
            sa.Column("effective_from", sa.Date(), nullable=True),
            sa.Column("effective_to", sa.Date(), nullable=True),
            sa.Column("status", sa.String(length=50), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.UniqueConstraint("rule_code", name="uq_rul_commission_rule_rule_code"),
        )
        op.create_index("ix_rul_commission_rule_rule_code", "rul_commission_rule", ["rule_code"])

    if "rul_gst_rule" not in inspector.get_table_names():
        op.create_table(
            "rul_gst_rule",
            sa.Column("gst_rule_id", sa.Integer(), primary_key=True, index=True),
            sa.Column("rule_code", sa.String(length=100), nullable=False),
            sa.Column("rule_name", sa.String(length=255), nullable=False),
            sa.Column("rate", sa.Float(), nullable=False, server_default="0"),
            sa.Column("applicability", sa.String(length=100), nullable=True),
            sa.Column("reverse_charge", sa.Boolean(), nullable=True, server_default=sa.false()),
            sa.Column("effective_from", sa.Date(), nullable=True),
            sa.Column("effective_to", sa.Date(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.UniqueConstraint("rule_code", name="uq_rul_gst_rule_rule_code"),
        )
        op.create_index("ix_rul_gst_rule_rule_code", "rul_gst_rule", ["rule_code"])

    if "rul_tds_rule" not in inspector.get_table_names():
        op.create_table(
            "rul_tds_rule",
            sa.Column("tds_rule_id", sa.Integer(), primary_key=True, index=True),
            sa.Column("rule_code", sa.String(length=100), nullable=False),
            sa.Column("rule_name", sa.String(length=255), nullable=False),
            sa.Column("section", sa.String(length=50), nullable=True),
            sa.Column("rate", sa.Float(), nullable=False, server_default="0"),
            sa.Column("threshold", sa.Float(), nullable=True),
            sa.Column("effective_from", sa.Date(), nullable=True),
            sa.Column("effective_to", sa.Date(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.UniqueConstraint("rule_code", name="uq_rul_tds_rule_rule_code"),
        )
        op.create_index("ix_rul_tds_rule_rule_code", "rul_tds_rule", ["rule_code"])


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "rul_tds_rule" in inspector.get_table_names():
        op.drop_table("rul_tds_rule")
    if "rul_gst_rule" in inspector.get_table_names():
        op.drop_table("rul_gst_rule")
    if "rul_commission_rule" in inspector.get_table_names():
        op.drop_table("rul_commission_rule")
    if "rul_validation_rule" in inspector.get_table_names():
        op.drop_table("rul_validation_rule")
