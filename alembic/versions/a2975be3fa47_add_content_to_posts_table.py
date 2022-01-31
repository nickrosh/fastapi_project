"""add content to posts table

Revision ID: a2975be3fa47
Revises: 62a6725f5590
Create Date: 2022-01-30 18:40:49.345252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2975be3fa47'
down_revision = '62a6725f5590'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
