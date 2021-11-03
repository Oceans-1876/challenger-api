"""Change Description length

Revision ID: 5f37b194b830
Revises: 1ffd1a52fe93
Create Date: 2021-11-03 19:28:42.471644+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f37b194b830'
down_revision = '1ffd1a52fe93'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_sources', 'description',
               existing_type=sa.VARCHAR(length=2000),
               type_=sa.String(length=3000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('data_sources', 'description',
               existing_type=sa.String(length=3000),
               type_=sa.VARCHAR(length=2000),
               existing_nullable=True)
    # ### end Alembic commands ###
