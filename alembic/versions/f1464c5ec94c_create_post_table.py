"""create post table

Revision ID: f1464c5ec94c
Revises: 
Create Date: 2022-11-12 17:38:22.875472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1464c5ec94c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('post')
    pass
