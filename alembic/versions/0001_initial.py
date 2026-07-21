"""Initial models migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-07-19 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'trn_tally_export_batch',
        sa.Column('batch_id', sa.Integer(), primary_key=True, index=True),
        sa.Column('batch_number', sa.String(length=100), nullable=True, unique=True, index=True),
        sa.Column('batch_name', sa.String(length=255), nullable=False),
        sa.Column('export_type', sa.String(length=50), nullable=False),
        sa.Column('period_start', sa.Date(), nullable=False),
        sa.Column('period_end', sa.Date(), nullable=False),
        sa.Column('total_records', sa.Integer(), nullable=True),
        sa.Column('exported_records', sa.Integer(), nullable=True),
        sa.Column('export_status', sa.String(length=50), nullable=True),
        sa.Column('sync_status', sa.String(length=50), nullable=True),
        sa.Column('file_path', sa.String(length=500), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'trn_tally_export_detail',
        sa.Column('detail_id', sa.Integer(), primary_key=True, index=True),
        sa.Column('batch_id', sa.Integer(), nullable=False, index=True),
        sa.Column('source_table', sa.String(length=100), nullable=False),
        sa.Column('source_id', sa.Integer(), nullable=False),
        sa.Column('exported_data', sa.Text(), nullable=True),
        sa.Column('export_status', sa.String(length=50), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )


def downgrade():
    op.drop_table('trn_tally_export_detail')
    op.drop_table('trn_tally_export_batch')
