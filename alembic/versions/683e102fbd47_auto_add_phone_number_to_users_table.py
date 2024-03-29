"""auto add phone number to users table

Revision ID: 683e102fbd47
Revises: 206786792710
Create Date: 2022-11-12 17:54:11.516025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '683e102fbd47'
down_revision = '206786792710'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###
