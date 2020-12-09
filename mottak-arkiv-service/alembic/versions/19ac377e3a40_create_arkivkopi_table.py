"""create transfer request table

Revision ID: 19ac377e3a40
Revises: f0ecc7d899bf
Create Date: 2020-11-29 11:59:43.324946

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '19ac377e3a40'
down_revision = 'f0ecc7d899bf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('arkivkopi',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('arkivuttrekk_id', sa.Integer(), nullable=False),
                    sa.Column('status',
                              sa.Enum('Bestilt', 'Startet', 'OK', 'Avbrutt', 'Feilet', name='arkivkopi_status_type',
                                      create_type=False), nullable=False),
                    sa.Column('storage_account', sa.String(), nullable=False),
                    sa.Column('container', sa.String(), nullable=False),
                    sa.Column('sas_token_start', sa.String(), nullable=False),
                    sa.Column('sas_token_slutt', sa.String(), nullable=False),
                    sa.Column('opprettet', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('endret', sa.DateTime(), server_default=sa.text('now()'), onupdate=sa.text('now()'),
                              nullable=False),
                    sa.ForeignKeyConstraint(['arkivuttrekk_id'], ['arkivuttrekk.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )


def downgrade():
    op.drop_table('arkivkopi')
    op.execute("drop type arkivkopi_status_type")
