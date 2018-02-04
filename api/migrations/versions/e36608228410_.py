"""empty message

Revision ID: e36608228410
Revises: 
Create Date: 2018-02-02 22:53:19.660052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e36608228410'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('request_akamaiCCU',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('request_number', sa.String(length=20), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('request_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_akamaiCCU')
    # ### end Alembic commands ###
