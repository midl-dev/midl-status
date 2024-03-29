"""empty message

Revision ID: b8bc19bdb95a
Revises: 
Create Date: 2023-07-30 18:26:14.573995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8bc19bdb95a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cluster_status',
    sa.Column('cluster', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('cluster', 'time')
    )
    op.create_table('request_counts',
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('cluster', sa.String(length=100), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('cluster', 'time')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request_counts')
    op.drop_table('cluster_status')
    # ### end Alembic commands ###
