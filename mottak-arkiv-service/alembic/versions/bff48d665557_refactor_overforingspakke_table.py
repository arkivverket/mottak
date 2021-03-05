"""refactor overforingspakke table by adding invitasjon_id with a foreign key constraint to invitasjon table and removes arkivuttrekk_id

Revision ID: bff48d665557
Revises: f2d569907a5c
Create Date: 2021-03-03 08:12:52.476199

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bff48d665557'
down_revision = '412b6ec6c2be'
branch_labels = None
depends_on = None


def upgrade():
    # add invitasjon_id
    op.add_column('overforingspakke', sa.Column('invitasjon_id', sa.Integer(), nullable=True, unique=True))
    op.execute('UPDATE overforingspakke '
               'SET invitasjon_id=( SELECT id '
               '                    FROM invitasjon '
               '                    WHERE overforingspakke.arkivuttrekk_id=invitasjon.arkivuttrekk_id '
               '                    ORDER BY invitasjon.opprettet DESC limit 1)')
    op.alter_column('overforingspakke', 'invitasjon_id', nullable=False)
    op.create_foreign_key('overforingspakke_invitasjon_id_fkey', 'overforingspakke', 'invitasjon', ['invitasjon_id'], ['id'], )

    # drop arkivuttrekk_id
    op.drop_constraint('overforingspakke_arkivuttrekk_id_fkey', 'overforingspakke', )
    op.drop_column('overforingspakke', 'arkivuttrekk_id')

def downgrade():
    # add arkivuttrekk_id
    op.add_column('overforingspakke', sa.Column('arkivuttrekk_id', sa.Integer(), nullable=True, unique=True))
    op.execute('UPDATE overforingspakke '
               'SET arkivuttrekk_id=( SELECT arkivuttrekk_id '
               '                      FROM invitasjon '
               '                      WHERE overforingspakke.invitasjon_id=invitasjon.id '
               '                      ORDER BY invitasjon.opprettet DESC limit 1)')
    op.alter_column('overforingspakke', 'arkivuttrekk_id', nullable=False)
    op.create_foreign_key('overforingspakke_arkivuttrekk_id_fkey', 'overforingspakke', 'arkivuttrekk', ['arkivuttrekk_id'],
                          ['id'], )

    # drop invitasjon_id
    op.drop_constraint('overforingspakke_invitasjon_id_fkey', 'overforingspakke', )
    op.drop_column('overforingspakke', 'invitasjon_id')
