"""IMP-6.2 login history audit columns

Revision ID: 0006_imp_62
Revises: 0005_imp_5b
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0006_imp_62"
down_revision = "0005_imp_5b"
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

    if not _has_table(inspector, "sec_login_history"):
        return

    if not _has_column(inspector, "sec_login_history", "username"):
        op.add_column("sec_login_history", sa.Column("username", sa.String(length=50), nullable=True))
    if not _has_column(inspector, "sec_login_history", "user_agent"):
        op.add_column("sec_login_history", sa.Column("user_agent", sa.String(length=255), nullable=True))
    if not _has_column(inspector, "sec_login_history", "failure_reason"):
        op.add_column("sec_login_history", sa.Column("failure_reason", sa.String(length=100), nullable=True))

    if not _has_index(inspector, "sec_login_history", "ix_sec_login_history_username"):
        op.create_index("ix_sec_login_history_username", "sec_login_history", ["username"], unique=False)

    try:
        op.alter_column("sec_login_history", "user_id", existing_type=sa.Integer(), nullable=True)
    except Exception:
        # SQLite and legacy schemas may not support direct alter; nullable relaxation is best-effort.
        pass


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "sec_login_history"):
        return

    if _has_index(inspector, "sec_login_history", "ix_sec_login_history_username"):
        op.drop_index("ix_sec_login_history_username", table_name="sec_login_history")

    if _has_column(inspector, "sec_login_history", "failure_reason"):
        op.drop_column("sec_login_history", "failure_reason")
    if _has_column(inspector, "sec_login_history", "user_agent"):
        op.drop_column("sec_login_history", "user_agent")
    if _has_column(inspector, "sec_login_history", "username"):
        op.drop_column("sec_login_history", "username")
