"""refactor arkivkopi table by adding invitasjon_id and target_name, and removing arkivuttrekk_id

Revision ID: ee70a0e9cb7b
Revises: bff48d665557
Create Date: 2021-03-03 10:10:52.128799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee70a0e9cb7b'
down_revision = 'bff48d665557'
branch_labels = None
depends_on = None


def upgrade():
    # add invitasjon_id
    op.add_column('arkivkopi', sa.Column('invitasjon_id', sa.Integer(), nullable=True))
    op.execute('UPDATE arkivkopi '
               'SET invitasjon_id=( SELECT id '
               '                    FROM invitasjon '
               '                    WHERE arkivkopi.arkivuttrekk_id=invitasjon.arkivuttrekk_id '
               '                    ORDER BY invitasjon.opprettet DESC limit 1)')
    op.alter_column('arkivkopi', 'invitasjon_id', nullable=False)
    op.create_foreign_key('arkivkopi_invitasjon_id_fkey', 'arkivkopi', 'invitasjon', ['invitasjon_id'], ['id'], )

    # add target_name
    op.add_column('arkivkopi', sa.Column('target_name', sa.String(), nullable=True))
    # sets target_name and assumes all existing rows are archives
    op.execute('UPDATE arkivkopi '
               'SET target_name=( SELECT obj_id::text '
               '                  FROM arkivuttrekk '
               '                  WHERE arkivuttrekk.id=arkivkopi.arkivuttrekk_id)')
    op.execute("UPDATE arkivkopi "
               "SET target_name=CONCAT(target_name, '/')")
    op.alter_column('arkivkopi', 'target_name', nullable=False)

    # add is_object, assumes all rows are archives
    op.add_column('arkivkopi', sa.Column('is_object', sa.Boolean(), nullable=True))
    op.execute('UPDATE arkivkopi SET is_object=false')
    op.alter_column('arkivkopi', 'is_object', nullable=False)

    # remove arkivuttrekk_id
    op.drop_constraint('arkivkopi_arkivuttrekk_id_fkey', 'arkivkopi', )
    op.drop_column('arkivkopi', 'arkivuttrekk_id')


def downgrade():
    # add arkivuttrekk_id
    op.add_column('arkivkopi', sa.Column('arkivuttrekk_id', sa.Integer(), nullable=True))
    op.execute('UPDATE arkivkopi '
               'SET arkivuttrekk_id=( SELECT arkivuttrekk_id '
               '                      FROM invitasjon '
               '                      WHERE arkivkopi.invitasjon_id=invitasjon.id '
               '                      ORDER BY invitasjon.opprettet DESC limit 1)')
    op.alter_column('arkivkopi', 'arkivuttrekk_id', nullable=False)
    op.create_foreign_key('arkivkopi_arkivuttrekk_id_fkey', 'arkivkopi', 'arkivuttrekk', ['arkivuttrekk_id'], ['id'], )

    # remove invitasjon_id
    op.drop_constraint('arkivkopi_invitasjon_id_fkey', 'arkivkopi', )
    op.drop_column('arkivkopi', 'invitasjon_id')

    # remove target_name
    op.drop_column('arkivkopi', 'target_name')

    # remove is_object
    op.drop_column('arkivkopi', 'is_object')
    pass
