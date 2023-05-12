"""add last column like in orginal schema

Revision ID: f4d4e6ff0857
Revises: 81f9854ae908
Create Date: 2023-05-10 22:03:03.054004

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4d4e6ff0857'
down_revision = '81f9854ae908'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", 
                  sa.Column("published", sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=False),nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
