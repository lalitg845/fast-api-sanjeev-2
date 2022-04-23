"""add content column to post table

Revision ID: 9a9a587c5e14
Revises: b555d29b395e
Create Date: 2022-04-21 13:45:37.531763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a9a587c5e14'
down_revision = 'b555d29b395e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
