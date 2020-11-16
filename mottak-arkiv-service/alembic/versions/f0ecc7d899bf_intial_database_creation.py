"""Intial database creation

Revision ID: f0ecc7d899bf
Revises:
Create Date: 2020-09-14 11:59:40.128185

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f0ecc7d899bf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metadatafil',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('type', sa.Enum('xml/mets', name='metadata_type_type'), nullable=False),
                    sa.Column('innhold', sa.Text(), nullable=False),
                    sa.Column('filnavn', sa.String(), nullable=False),
                    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('arkivuttrekk',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('obj_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('status', sa.Enum('Opprettet', 'Under behandling', 'Avvist', 'Sendt til bevaring',
                                                name='arkivuttrekk_status_type'), nullable=False),
                    sa.Column('type', sa.Enum('Noark3', 'Noark5', 'Fagsystem', "SIARD", name='arkivvuttrekk_type_type'),
                              nullable=False),
                    sa.Column('tittel', sa.String(), nullable=False),
                    sa.Column('sjekksum_sha256', sa.String(length=64), nullable=False),
                    sa.Column('avgiver_navn', sa.String(), nullable=False),
                    sa.Column('avgiver_epost', sa.String(), nullable=False),
                    sa.Column('koordinator_epost', sa.String(), nullable=False),
                    sa.Column('metadatafil_id', sa.Integer(), nullable=False),
                    sa.Column('arkiv_startdato', sa.Date(), nullable=False),
                    sa.Column('arkiv_sluttdato', sa.Date(), nullable=False),
                    sa.Column('storrelse', sa.Float(), nullable=False),
                    sa.Column('avtalenummer', sa.String(), nullable=False),
                    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('endret', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['metadatafil_id'], ['metadatafil.id']),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('metadatafil_id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_index(op.f('ix_arkivuttrekk_obj_id'), 'arkivuttrekk', ['obj_id'], unique=True)
    op.create_index(op.f('ix_arkivuttrekk_status'), 'arkivuttrekk', ['status'], unique=False)
    op.create_table('invitasjon',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('ekstern_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
                    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=False),
                    sa.Column('status', sa.Enum('Sendt', 'Feilet', name='invitasjon_status_type'), nullable=False),
                    sa.Column('avgiver_epost', sa.String(), nullable=False),
                    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id'),
                    sa.UniqueConstraint('ekstern_id')
                    )
    op.create_table('lokasjon',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=False),
                    sa.Column('objecktlager', sa.String(), nullable=False),
                    sa.Column('generasjon', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('arkivuttrekk_id', 'generasjon', name='arkivuttrekk_id_generasjon_uc'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('overforingspakke',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=False),
                    sa.Column('tusd_id', sa.String(length=60), nullable=False, index=True),
                    sa.Column('navn', sa.String(), nullable=False),
                    sa.Column('storrelse', sa.BigInteger(), nullable=False),
                    sa.Column('status', sa.Enum('Startet', 'OK', 'Avbrutt', 'Feilet', name='overforingspakke_status_type'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('arkivuttrekk_id'),
                    sa.UniqueConstraint('tusd_id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('tester',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=False),
                    sa.Column('epost', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tester')
    op.drop_table('overforingspakke')
    op.drop_table('lokasjon')
    op.drop_table('invitasjon')
    op.drop_index(op.f('ix_arkivuttrekk_status'), table_name='arkivuttrekk')
    op.drop_index(op.f('ix_arkivuttrekk_obj_id'), table_name='arkivuttrekk')
    op.drop_table('arkivuttrekk')
    op.drop_table('metadatafil')

    op.execute('drop type arkivuttrekk_status_type')
    op.execute('drop type arkivvuttrekk_type_type')
    op.execute('drop type overforingspakke_status_type')
    op.execute('drop type metadata_type_type')
    op.execute('drop type invitasjon_status_type')

    # Drop enum types on downgrade.
    # ### end Alembic commands ###
