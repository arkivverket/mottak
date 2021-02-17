"""rename column name in overforingspakke

Revision ID: 412b6ec6c2be
Revises: 19ac377e3a40
Create Date: 2021-02-16 15:15:54.172642

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '412b6ec6c2be'
down_revision = '19ac377e3a40'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('overforingspakke', 'navn', new_column_name='tusd_objekt_navn')


def downgrade():
    op.alter_column('overforingspakke', 'tusd_objekt_navn', new_column_name='navn')

