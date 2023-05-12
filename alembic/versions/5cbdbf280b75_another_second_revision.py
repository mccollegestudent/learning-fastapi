"""another second revision

Revision ID: 5cbdbf280b75
Revises: ad2603c7df34
Create Date: 2023-05-10 20:43:22.240927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cbdbf280b75'
down_revision = 'ad2603c7df34'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
