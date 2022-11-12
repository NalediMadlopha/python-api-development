"""add foreign key to post table

Revision ID: 07b0ad4ced3c
Revises: 94c2773bb040
Create Date: 2022-11-12 17:43:48.250079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b0ad4ced3c'
down_revision = '94c2773bb040'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='post', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_column('post', 'owner_id')
    op.drop_constraint('post_users_fk', table_name='post')
    pass