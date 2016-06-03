"""add user_id to drink_log

Revision ID: 78b2eab178fd
Revises: 
Create Date: 2016-05-27 13:13:57.166659

"""

# revision identifiers, used by Alembic.
revision = '78b2eab178fd'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('drink_log', sa.Column('user_id', sa.Integer(), nullable=True))
    with op.batch_alter_table('fp_user'):
    	op.create_foreign_key(None, 'drink_log', 'fp_user', ['user_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'drink_log', type_='foreignkey')
    op.drop_column('drink_log', 'user_id')
    ### end Alembic commands ###
