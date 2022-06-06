"""modify column

Revision ID: 986441aa7483
Revises: 39287eb108c7
Create Date: 2022-06-02 13:48:46.917917+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '986441aa7483'
down_revision = '39287eb108c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('species_extra', 'unaccepted_reason',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.Text(),
               existing_nullable=True)
    op.drop_index('idx_stations_coordinates', table_name='stations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('idx_stations_coordinates', 'stations', ['coordinates'], unique=False)
    op.alter_column('species_extra', 'unaccepted_reason',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    # ### end Alembic commands ###
