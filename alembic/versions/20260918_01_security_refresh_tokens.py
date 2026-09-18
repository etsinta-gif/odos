"""Create refresh-token storage for authentication.

Revision ID: 20260918_01_security_refresh_tokens
Revises: 0009_imp_intel_3
Create Date: 2026-09-18
"""

from alembic import op
import sqlalchemy as sa


revision = "20260918_01_security_refresh_tokens"
down_revision = "0009_imp_intel_3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "sec_refresh_tokens" not in inspector.get_table_names():
        op.create_table(
            "sec_refresh_tokens",
            sa.Column("token_id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("token_hash", sa.String(length=255), nullable=False),
            sa.Column("issued_at", sa.DateTime(), nullable=False),
            sa.Column("expires_at", sa.DateTime(), nullable=False),
            sa.Column("revoked_at", sa.DateTime(), nullable=True),
            sa.Column("replaced_by_hash", sa.String(length=255), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["sec_users.user_id"]),
            sa.PrimaryKeyConstraint("token_id"),
            sa.UniqueConstraint("token_hash"),
        )

    indexes = {index["name"] for index in sa.inspect(bind).get_indexes("sec_refresh_tokens")}
    if "ix_sec_refresh_tokens_user_id" not in indexes:
        op.create_index("ix_sec_refresh_tokens_user_id", "sec_refresh_tokens", ["user_id"], unique=False)
    if "ix_sec_refresh_tokens_token_hash" not in indexes:
        op.create_index("ix_sec_refresh_tokens_token_hash", "sec_refresh_tokens", ["token_hash"], unique=True)
    if "ix_sec_refresh_tokens_expires_at" not in indexes:
        op.create_index("ix_sec_refresh_tokens_expires_at", "sec_refresh_tokens", ["expires_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_sec_refresh_tokens_expires_at", table_name="sec_refresh_tokens")
    op.drop_index("ix_sec_refresh_tokens_token_hash", table_name="sec_refresh_tokens")
    op.drop_index("ix_sec_refresh_tokens_user_id", table_name="sec_refresh_tokens")
    op.drop_table("sec_refresh_tokens")