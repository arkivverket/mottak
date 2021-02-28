"""add column filnavn to arkivkopi

Revision ID: f2d569907a5c
Revises: 412b6ec6c2be
Create Date: 2021-02-28 21:08:05.338956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2d569907a5c'
down_revision = '412b6ec6c2be'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('arkivkopi',
                  sa.Column('filnavn', sa.String(), nullable=True))
    op.execute("UPDATE arkivkopi SET filnavn = 'filnavn.tar'")
    op.alter_column('arkivkopi', 'filnavn', nullable=False)


def downgrade():
    op.drop_column('arkivkopi', 'filnavn')
