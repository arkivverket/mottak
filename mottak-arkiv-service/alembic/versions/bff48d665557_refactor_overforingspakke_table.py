"""refactor overforingspakke table

Revision ID: bff48d665557
Revises: f2d569907a5c
Create Date: 2021-03-03 08:12:52.476199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bff48d665557'
down_revision = 'f2d569907a5c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('overforingspakke', sa.Column('invitasjon_id', sa.Integer(), nullable=True))
    op.execute('INSERT INTO overforingspakke (id, arkivuttrekk_id, invitasjon_id, tusd_id, tusd_objekt_navn, storrelse, status, opprettet, endret)  '
               'SELECT o.id, o.arkivuttrekk_id, i.id, o.tusd_id, o.tusd_objekt_navn, o.storrelse, o.status, o.opprettet, o.endret '
               'FROM invitasjon i, overforingspakke o '
               'WHERE i.arkivuttrekk_id=o.arkivuttrekk_id')



def downgrade():
    op.drop_column('overforingspakke', 'invitasjon_id')
