"""empty message

Revision ID: 09506978ab67
Revises: 1bbf7f710ae5
Create Date: 2024-08-22 08:54:30.761139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09506978ab67'
down_revision = '1bbf7f710ae5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('Person')
    with op.batch_alter_table('Favorite', schema=None) as batch_op:
        batch_op.drop_constraint('Favorite_people_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'people', ['people_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Favorite', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('Favorite_people_id_fkey', 'Person', ['people_id'], ['id'])

    op.create_table('Person',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Person_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('birth_year', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('eye_color', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('gender', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('hair_color', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('height', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('homeworld', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('mass', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('skin_color', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='Person_pkey')
    )
    op.drop_table('people')
    # ### end Alembic commands ###
