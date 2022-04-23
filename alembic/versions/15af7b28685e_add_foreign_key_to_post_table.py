"""add foreign-key to post table

Revision ID: 15af7b28685e
Revises: 698af889acd0
Create Date: 2022-04-21 14:18:58.419742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15af7b28685e'
down_revision = '698af889acd0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
