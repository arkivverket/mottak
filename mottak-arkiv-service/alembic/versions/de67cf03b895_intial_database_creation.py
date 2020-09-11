"""Intial database creation

Revision ID: de67cf03b895
Revises: 
Create Date: 2020-09-11 19:58:00.762500

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'de67cf03b895'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('arkivuttrekk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('obj_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('type', sa.Enum('Noark3', 'Noark5', 'Fagsystem'), nullable=False),
    sa.Column('tittel', sa.String(), nullable=False),
    sa.Column('beskrivelse', sa.String(), nullable=False),
    sa.Column('sjekksum', sa.String(length=64), nullable=False),
    sa.Column('avgiver_navn', sa.String(), nullable=False),
    sa.Column('avgiver_epost', sa.String(), nullable=False),
    sa.Column('koordinator_epost', sa.String(), nullable=False),
    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('endret', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_arkivuttrekk_id'), 'arkivuttrekk', ['id'], unique=False)
    op.create_index(op.f('ix_arkivuttrekk_obj_id'), 'arkivuttrekk', ['obj_id'], unique=False)
    op.create_table('invitasjon',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('arkiv_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('Sent', 'Feilet'), nullable=False),
    sa.ForeignKeyConstraint(['arkiv_id'], ['arkivuttrekk.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('arkiv_id')
    )
    op.create_index(op.f('ix_invitasjon_id'), 'invitasjon', ['id'], unique=False)
    op.create_table('lokasjon',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=True),
    sa.Column('kontainer', sa.String(), nullable=False),
    sa.Column('generasjon', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lokasjon_id'), 'lokasjon', ['id'], unique=False)
    op.create_table('metadatafil',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.Enum('xml/mets'), nullable=False),
    sa.Column('innhold', sa.Text(), nullable=False),
    sa.Column('filnavn', sa.String(), nullable=False),
    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_metadatafil_id'), 'metadatafil', ['id'], unique=False)
    op.create_table('overforingspakke',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=True),
    sa.Column('navn', sa.String(), nullable=False),
    sa.Column('storrelse', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OK', 'Avbrutt', 'Feilet'), nullable=False),
    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('arkivuttrekk_id')
    )
    op.create_index(op.f('ix_overforingspakke_id'), 'overforingspakke', ['id'], unique=False)
    op.create_table('tester',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('epost', sa.String(), nullable=True),
    sa.Column('arkiv_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['arkiv_id'], ['arkivuttrekk.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tester_id'), 'tester', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tester_id'), table_name='tester')
    op.drop_table('tester')
    op.drop_index(op.f('ix_overforingspakke_id'), table_name='overforingspakke')
    op.drop_table('overforingspakke')
    op.drop_index(op.f('ix_metadatafil_id'), table_name='metadatafil')
    op.drop_table('metadatafil')
    op.drop_index(op.f('ix_lokasjon_id'), table_name='lokasjon')
    op.drop_table('lokasjon')
    op.drop_index(op.f('ix_invitasjon_id'), table_name='invitasjon')
    op.drop_table('invitasjon')
    op.drop_index(op.f('ix_arkivuttrekk_obj_id'), table_name='arkivuttrekk')
    op.drop_index(op.f('ix_arkivuttrekk_id'), table_name='arkivuttrekk')
    op.drop_table('arkivuttrekk')
    # ### end Alembic commands ###
