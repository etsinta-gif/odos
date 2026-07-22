"""IMP-INTEL-1 phase 1 schema additions

Revision ID: 0007_imp_intel_1
Revises: 0006_imp_62
Create Date: 2026-07-22
"""

from alembic import op
import sqlalchemy as sa


revision = "0007_imp_intel_1"
down_revision = "0006_imp_62"
branch_labels = None
depends_on = None


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


def _ensure_column(inspector, table_name, column):
    if _has_table(inspector, table_name) and not _has_column(inspector, table_name, column.name):
        op.add_column(table_name, column)


def _ensure_index(inspector, table_name, index_name, columns):
    if _has_table(inspector, table_name) and not _has_index(inspector, table_name, index_name):
        op.create_index(index_name, table_name, columns, unique=False)


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "mst_party"):
        op.create_table(
            "mst_party",
            sa.Column("party_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("pan", sa.String(length=20), nullable=False),
            sa.Column("gstin", sa.String(length=30), nullable=True),
            sa.Column("classification", sa.String(length=50), nullable=False, server_default="Unknown"),
            sa.Column("default_gst_rate", sa.Numeric(5, 2), nullable=False, server_default="0"),
            sa.Column("default_tds_rate", sa.Numeric(5, 2), nullable=False, server_default="0"),
            sa.Column("max_commission", sa.Numeric(15, 2), nullable=True),
            sa.Column("metadata", sa.JSON(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=True, server_default=sa.true()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.UniqueConstraint("company_id", "pan", name="uq_mst_party_company_pan"),
        )
        op.create_index("ix_mst_party_company_id", "mst_party", ["company_id"], unique=False)
        op.create_index("ix_mst_party_pan", "mst_party", ["pan"], unique=False)
        op.create_index("ix_mst_party_created_by", "mst_party", ["created_by"], unique=False)
        op.create_index("ix_mst_party_updated_by", "mst_party", ["updated_by"], unique=False)

    _ensure_column(inspector, "mst_lender", sa.Column("default_gst_rate", sa.Numeric(5, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "mst_lender", sa.Column("default_tds_rate", sa.Numeric(5, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "mst_lender", sa.Column("max_commission", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "mst_lender", sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"))

    _ensure_column(inspector, "mst_connector", sa.Column("default_gst_rate", sa.Numeric(5, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "mst_connector", sa.Column("default_tds_rate", sa.Numeric(5, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "mst_connector", sa.Column("max_commission", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "mst_connector", sa.Column("metadata", sa.JSON(), nullable=False, server_default="{}"))

    _ensure_column(inspector, "trn_revenue", sa.Column("party_id", sa.Integer(), nullable=True))
    _ensure_index(inspector, "trn_revenue", "ix_trn_revenue_party_id", ["party_id"])
    _ensure_column(inspector, "trn_revenue", sa.Column("reported_amount", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "trn_revenue", sa.Column("reported_gst", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_revenue", sa.Column("reported_tds", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_revenue", sa.Column("reported_net", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "trn_revenue", sa.Column("system_gst", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_revenue", sa.Column("system_tds", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_revenue", sa.Column("gst_match", sa.Boolean(), nullable=False, server_default=sa.false()))
    _ensure_column(inspector, "trn_revenue", sa.Column("tds_match", sa.Boolean(), nullable=False, server_default=sa.false()))
    _ensure_column(inspector, "trn_revenue", sa.Column("data", sa.JSON(), nullable=False, server_default="{}"))

    _ensure_column(inspector, "trn_commission", sa.Column("party_id", sa.Integer(), nullable=True))
    _ensure_index(inspector, "trn_commission", "ix_trn_commission_party_id", ["party_id"])
    _ensure_column(inspector, "trn_commission", sa.Column("reported_commission", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "trn_commission", sa.Column("reported_gst", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_commission", sa.Column("reported_tds", sa.Numeric(15, 2), nullable=False, server_default="0"))
    _ensure_column(inspector, "trn_commission", sa.Column("reported_net", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "trn_commission", sa.Column("exceeds_max", sa.Boolean(), nullable=False, server_default=sa.false()))
    _ensure_column(inspector, "trn_commission", sa.Column("gst_match", sa.Boolean(), nullable=False, server_default=sa.false()))
    _ensure_column(inspector, "trn_commission", sa.Column("tds_match", sa.Boolean(), nullable=False, server_default=sa.false()))
    _ensure_column(inspector, "trn_commission", sa.Column("data", sa.JSON(), nullable=False, server_default="{}"))

    _ensure_column(inspector, "trn_payment", sa.Column("case_id", sa.Integer(), nullable=True))
    _ensure_index(inspector, "trn_payment", "ix_trn_payment_case_id", ["case_id"])
    _ensure_column(inspector, "trn_payment", sa.Column("party_id", sa.Integer(), nullable=True))
    _ensure_index(inspector, "trn_payment", "ix_trn_payment_party_id", ["party_id"])
    _ensure_column(inspector, "trn_payment", sa.Column("amount", sa.Numeric(15, 2), nullable=True))
    _ensure_column(inspector, "trn_payment", sa.Column("mode", sa.String(length=50), nullable=True))
    _ensure_column(inspector, "trn_payment", sa.Column("data", sa.JSON(), nullable=False, server_default="{}"))

    if not _has_table(inspector, "etl_red_flag"):
        op.create_table(
            "etl_red_flag",
            sa.Column("red_flag_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("batch_guid", sa.String(length=64), nullable=True),
            sa.Column("record_type", sa.String(length=50), nullable=False),
            sa.Column("record_id", sa.Integer(), nullable=False),
            sa.Column("severity", sa.String(length=20), nullable=False),
            sa.Column("category", sa.String(length=50), nullable=False),
            sa.Column("message", sa.Text(), nullable=False),
            sa.Column("field", sa.String(length=100), nullable=True),
            sa.Column("reported_value", sa.String(length=100), nullable=True),
            sa.Column("expected_value", sa.String(length=100), nullable=True),
            sa.Column("status", sa.String(length=20), nullable=False, server_default="OPEN"),
            sa.Column("resolution_notes", sa.Text(), nullable=True),
            sa.Column("resolved_by", sa.Integer(), nullable=True),
            sa.Column("resolved_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )
        op.create_index("ix_etl_red_flag_company_id", "etl_red_flag", ["company_id"], unique=False)
        op.create_index("ix_etl_red_flag_batch_guid", "etl_red_flag", ["batch_guid"], unique=False)
        op.create_index("ix_etl_red_flag_record_type", "etl_red_flag", ["record_type"], unique=False)
        op.create_index("ix_etl_red_flag_record_id", "etl_red_flag", ["record_id"], unique=False)
        op.create_index("ix_etl_red_flag_severity", "etl_red_flag", ["severity"], unique=False)
        op.create_index("ix_etl_red_flag_category", "etl_red_flag", ["category"], unique=False)
        op.create_index("ix_etl_red_flag_status", "etl_red_flag", ["status"], unique=False)
        op.create_index("ix_etl_red_flag_resolved_by", "etl_red_flag", ["resolved_by"], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_table(inspector, "etl_red_flag"):
        for index_name in [
            "ix_etl_red_flag_resolved_by",
            "ix_etl_red_flag_status",
            "ix_etl_red_flag_category",
            "ix_etl_red_flag_severity",
            "ix_etl_red_flag_record_id",
            "ix_etl_red_flag_record_type",
            "ix_etl_red_flag_batch_guid",
            "ix_etl_red_flag_company_id",
        ]:
            if _has_index(inspector, "etl_red_flag", index_name):
                op.drop_index(index_name, table_name="etl_red_flag")
        op.drop_table("etl_red_flag")

    if _has_table(inspector, "mst_party"):
        for index_name in [
            "ix_mst_party_updated_by",
            "ix_mst_party_created_by",
            "ix_mst_party_pan",
            "ix_mst_party_company_id",
        ]:
            if _has_index(inspector, "mst_party", index_name):
                op.drop_index(index_name, table_name="mst_party")
        op.drop_table("mst_party")

    # Column rollback intentionally omitted for safety in SQLite-heavy environments.
