"""add the rest of the column to the post table

Revision ID: 94c2773bb040
Revises: a8aafb57663c
Create Date: 2022-11-12 17:42:44.154885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c2773bb040'
down_revision = 'a8aafb57663c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    op.add_column('post', sa.Column('published', sa.Boolean(), server_default='FALSE', default=False, nullable=False))
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                                    nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'content')
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
