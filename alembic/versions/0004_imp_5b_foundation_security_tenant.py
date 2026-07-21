"""IMP-5B foundation: security and tenant metadata columns

Revision ID: 0004_imp_5b
Revises: 0003_imp_510
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0004_imp_5b"
down_revision = "0003_imp_510"
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


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "sec_roles"):
        op.create_table(
            "sec_roles",
            sa.Column("role_id", sa.Integer(), primary_key=True),
            sa.Column("role_name", sa.String(length=50), nullable=False, unique=True),
            sa.Column("description", sa.String(length=255), nullable=True),
            sa.Column("is_system", sa.Boolean(), nullable=False, server_default=sa.false()),
            sa.Column("created_at", sa.DateTime(), nullable=True),
        )
        op.create_index("ix_sec_roles_role_name", "sec_roles", ["role_name"], unique=False)

    if not _has_table(inspector, "sec_permissions"):
        op.create_table(
            "sec_permissions",
            sa.Column("permission_id", sa.Integer(), primary_key=True),
            sa.Column("resource", sa.String(length=100), nullable=False),
            sa.Column("action", sa.String(length=50), nullable=False),
            sa.Column("description", sa.String(length=255), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.UniqueConstraint("resource", "action", name="uq_sec_permissions_resource_action"),
        )

    if not _has_table(inspector, "sec_users"):
        op.create_table(
            "sec_users",
            sa.Column("user_id", sa.Integer(), primary_key=True),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("username", sa.String(length=50), nullable=False, unique=True),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=True),
            sa.Column("full_name", sa.String(length=255), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("last_login", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("updated_at", sa.DateTime(), nullable=True),
        )
        op.create_index("ix_sec_users_username", "sec_users", ["username"], unique=False)
        op.create_index("ix_sec_users_company_id", "sec_users", ["company_id"], unique=False)

    if not _has_table(inspector, "user_roles"):
        op.create_table(
            "user_roles",
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("role_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["sec_users.user_id"]),
            sa.ForeignKeyConstraint(["role_id"], ["sec_roles.role_id"]),
            sa.PrimaryKeyConstraint("user_id", "role_id"),
        )

    if not _has_table(inspector, "role_permissions"):
        op.create_table(
            "role_permissions",
            sa.Column("role_id", sa.Integer(), nullable=False),
            sa.Column("permission_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["role_id"], ["sec_roles.role_id"]),
            sa.ForeignKeyConstraint(["permission_id"], ["sec_permissions.permission_id"]),
            sa.PrimaryKeyConstraint("role_id", "permission_id"),
        )

    if not _has_table(inspector, "sec_login_history"):
        op.create_table(
            "sec_login_history",
            sa.Column("login_id", sa.Integer(), primary_key=True),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("company_id", sa.Integer(), nullable=False),
            sa.Column("login_at", sa.DateTime(), nullable=True),
            sa.Column("auth_status", sa.String(length=20), nullable=False, server_default="SUCCESS"),
            sa.Column("source_ip", sa.String(length=100), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["sec_users.user_id"]),
        )

    if _has_table(inspector, "meta_import_template"):
        if not _has_column(inspector, "meta_import_template", "company_id"):
            op.add_column("meta_import_template", sa.Column("company_id", sa.Integer(), nullable=True))
        if not _has_column(inspector, "meta_import_template", "shared"):
            op.add_column(
                "meta_import_template",
                sa.Column("shared", sa.Boolean(), nullable=False, server_default=sa.false()),
            )
        if not _has_index(inspector, "meta_import_template", "ix_meta_import_template_company_id"):
            op.create_index("ix_meta_import_template_company_id", "meta_import_template", ["company_id"], unique=False)

    if _has_table(inspector, "meta_field_mapping"):
        if not _has_column(inspector, "meta_field_mapping", "company_id"):
            op.add_column("meta_field_mapping", sa.Column("company_id", sa.Integer(), nullable=True))
        if not _has_index(inspector, "meta_field_mapping", "ix_meta_field_mapping_company_id"):
            op.create_index("ix_meta_field_mapping_company_id", "meta_field_mapping", ["company_id"], unique=False)

    if _has_table(inspector, "etl_data_lineage"):
        if not _has_column(inspector, "etl_data_lineage", "company_id"):
            op.add_column(
                "etl_data_lineage",
                sa.Column("company_id", sa.Integer(), nullable=False, server_default="1"),
            )
        if not _has_index(inspector, "etl_data_lineage", "ix_etl_data_lineage_company_id"):
            op.create_index("ix_etl_data_lineage_company_id", "etl_data_lineage", ["company_id"], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_table(inspector, "etl_data_lineage"):
        if _has_index(inspector, "etl_data_lineage", "ix_etl_data_lineage_company_id"):
            op.drop_index("ix_etl_data_lineage_company_id", table_name="etl_data_lineage")
        if _has_column(inspector, "etl_data_lineage", "company_id"):
            op.drop_column("etl_data_lineage", "company_id")

    if _has_table(inspector, "meta_field_mapping") and _has_column(inspector, "meta_field_mapping", "company_id"):
        if _has_index(inspector, "meta_field_mapping", "ix_meta_field_mapping_company_id"):
            op.drop_index("ix_meta_field_mapping_company_id", table_name="meta_field_mapping")
        op.drop_column("meta_field_mapping", "company_id")

    if _has_table(inspector, "meta_import_template"):
        if _has_index(inspector, "meta_import_template", "ix_meta_import_template_company_id"):
            op.drop_index("ix_meta_import_template_company_id", table_name="meta_import_template")
        if _has_column(inspector, "meta_import_template", "shared"):
            op.drop_column("meta_import_template", "shared")
        if _has_column(inspector, "meta_import_template", "company_id"):
            op.drop_column("meta_import_template", "company_id")

    if _has_table(inspector, "sec_login_history"):
        op.drop_table("sec_login_history")
    if _has_table(inspector, "role_permissions"):
        op.drop_table("role_permissions")
    if _has_table(inspector, "user_roles"):
        op.drop_table("user_roles")
    if _has_table(inspector, "sec_users"):
        if _has_index(inspector, "sec_users", "ix_sec_users_company_id"):
            op.drop_index("ix_sec_users_company_id", table_name="sec_users")
        if _has_index(inspector, "sec_users", "ix_sec_users_username"):
            op.drop_index("ix_sec_users_username", table_name="sec_users")
        op.drop_table("sec_users")
    if _has_table(inspector, "sec_permissions"):
        op.drop_table("sec_permissions")
    if _has_table(inspector, "sec_roles"):
        if _has_index(inspector, "sec_roles", "ix_sec_roles_role_name"):
            op.drop_index("ix_sec_roles_role_name", table_name="sec_roles")
        op.drop_table("sec_roles")
