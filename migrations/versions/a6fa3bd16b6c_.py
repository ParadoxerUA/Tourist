"""empty message

Revision ID: a6fa3bd16b6c
Revises: 7c71bc2aee0e
Create Date: 2019-10-31 17:45:08.071704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6fa3bd16b6c'
down_revision = '7c71bc2aee0e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trip', 'admin_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trip', 'admin_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
