"""A generic, single-revision Alembic migration.

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
isolated_context = ${repr(isolated_context)}


def upgrade():
    pass


def downgrade():
    pass
