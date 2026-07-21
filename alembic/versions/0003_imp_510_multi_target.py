"""IMP-5.10 multi-target ETL support

Revision ID: 0003_imp_510
Revises: 0002_imp_59
Create Date: 2026-07-20
"""

from alembic import op
import sqlalchemy as sa


revision = "0003_imp_510"
down_revision = "0002_imp_59"
branch_labels = None
depends_on = None


def _has_column(inspector, table_name, column_name):
    if table_name not in inspector.get_table_names():
        return False
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def _create_reference_table(inspector, table_name):
    if table_name in inspector.get_table_names():
        return
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("code", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("code", name=f"uq_{table_name}_code"),
    )
    op.create_index(f"ix_{table_name}_code", table_name, ["code"])


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "etl_import_batch" in inspector.get_table_names() and not _has_column(inspector, "etl_import_batch", "template_id"):
        op.add_column("etl_import_batch", sa.Column("template_id", sa.Integer(), nullable=True))
        op.create_index("ix_etl_import_batch_template_id", "etl_import_batch", ["template_id"])

    if "mst_lender" in inspector.get_table_names() and not _has_column(inspector, "mst_lender", "dsa_code"):
        op.add_column("mst_lender", sa.Column("dsa_code", sa.String(length=100), nullable=True))

    if "mst_product" in inspector.get_table_names():
        if not _has_column(inspector, "mst_product", "sub_product"):
            op.add_column("mst_product", sa.Column("sub_product", sa.String(length=255), nullable=True))
        if not _has_column(inspector, "mst_product", "roi_percent"):
            op.add_column("mst_product", sa.Column("roi_percent", sa.Float(), nullable=True))

    if "rul_commission_rule" in inspector.get_table_names():
        for name, column in [
            ("slab_type", sa.Column("slab_type", sa.String(length=50), nullable=True)),
            ("base_percent", sa.Column("base_percent", sa.Float(), nullable=True)),
            ("headline_percent", sa.Column("headline_percent", sa.Float(), nullable=True)),
            ("pf_percent", sa.Column("pf_percent", sa.Float(), nullable=True)),
            ("i_percent", sa.Column("i_percent", sa.Float(), nullable=True)),
            ("qualifying_condition", sa.Column("qualifying_condition", sa.Text(), nullable=True)),
            ("qualifying_notes", sa.Column("qualifying_notes", sa.Text(), nullable=True)),
            ("commercial_terms", sa.Column("commercial_terms", sa.Text(), nullable=True)),
            ("clawback_conditions", sa.Column("clawback_conditions", sa.Text(), nullable=True)),
        ]:
            if not _has_column(inspector, "rul_commission_rule", name):
                op.add_column("rul_commission_rule", column)

    if "rul_commission_slab" in inspector.get_table_names():
        for name, column in [
            ("commission_rule_id", sa.Column("commission_rule_id", sa.Integer(), nullable=True)),
            ("tier_name", sa.Column("tier_name", sa.String(length=100), nullable=True)),
            ("tier_min", sa.Column("tier_min", sa.Float(), nullable=True)),
            ("tier_max", sa.Column("tier_max", sa.Float(), nullable=True)),
        ]:
            if not _has_column(inspector, "rul_commission_slab", name):
                op.add_column("rul_commission_slab", column)
        if not any(idx["name"] == "ix_rul_commission_slab_commission_rule_id" for idx in inspector.get_indexes("rul_commission_slab")):
            op.create_index("ix_rul_commission_slab_commission_rule_id", "rul_commission_slab", ["commission_rule_id"])

        indexes = {idx["name"] for idx in inspector.get_indexes("rul_commission_slab")}
        if "ix_rul_commission_slab_slab_label" not in indexes:
            op.create_index("ix_rul_commission_slab_slab_label", "rul_commission_slab", ["slab_label"])

        existing_uniques = {uc["name"] for uc in inspector.get_unique_constraints("rul_commission_slab") if uc.get("name")}
        if "uq_rul_commission_slab_rule_tier" not in existing_uniques:
            with op.batch_alter_table("rul_commission_slab") as batch_op:
                for uc in inspector.get_unique_constraints("rul_commission_slab"):
                    cols = uc.get("column_names") or []
                    if cols == ["slab_label"] and uc.get("name"):
                        batch_op.drop_constraint(uc["name"], type_="unique")
                batch_op.create_unique_constraint("uq_rul_commission_slab_rule_tier", ["commission_rule_id", "tier_name"])

    for table_name in [
        "ref_loan_type",
        "ref_channel",
        "ref_product_category",
        "ref_status",
        "ref_region",
        "ref_borrower_profile",
        "ref_loan_nature",
        "ref_location",
    ]:
        _create_reference_table(inspector, table_name)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name in [
        "ref_location",
        "ref_loan_nature",
        "ref_borrower_profile",
        "ref_region",
        "ref_status",
        "ref_product_category",
        "ref_channel",
        "ref_loan_type",
    ]:
        if table_name in inspector.get_table_names():
            op.drop_table(table_name)

    if "rul_commission_slab" in inspector.get_table_names() and any(idx["name"] == "ix_rul_commission_slab_commission_rule_id" for idx in inspector.get_indexes("rul_commission_slab")):
        op.drop_index("ix_rul_commission_slab_commission_rule_id", table_name="rul_commission_slab")

    if "etl_import_batch" in inspector.get_table_names() and any(idx["name"] == "ix_etl_import_batch_template_id" for idx in inspector.get_indexes("etl_import_batch")):
        op.drop_index("ix_etl_import_batch_template_id", table_name="etl_import_batch")