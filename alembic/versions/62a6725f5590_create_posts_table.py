"""create posts table

Revision ID: 62a6725f5590
Revises: 
Create Date: 2022-01-30 18:32:14.167068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62a6725f5590'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                                        primary_key=True), 
                            sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    pass
