"""add foreign-key to post table

Revision ID: 81f9854ae908
Revises: dbefac27149b
Create Date: 2023-05-10 21:47:39.018319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f9854ae908'
down_revision = 'dbefac27149b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", 
                          local_cols=['owner_id'], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
