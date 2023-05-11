"""empty message

Revision ID: 86b0ec486fc7
Revises: bf8caefeb8c0
Create Date: 2023-05-09 10:21:32.451225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86b0ec486fc7'
down_revision = 'bf8caefeb8c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('crystal', sa.Column('healer_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'crystal', 'healer', ['healer_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'crystal', type_='foreignkey')
    op.drop_column('crystal', 'healer_id')
    # ### end Alembic commands ###
