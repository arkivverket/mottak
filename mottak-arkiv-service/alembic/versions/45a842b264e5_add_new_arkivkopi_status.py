"""add new arkivkopi status

Revision ID: 45a842b264e5
Revises: 19ac377e3a40
Create Date: 2021-01-28 10:54:40.970366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45a842b264e5'
down_revision = '19ac377e3a40'
branch_labels = None
depends_on = None


def upgrade():
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE arkivkopi_status_type ADD VALUE 'Bestilling feilet'")


def downgrade():
    op.execute("ALTER TYPE arkivkopi_status_type RENAME TO arkivkopi_status_type_old")
    op.execute("CREATE TYPE arkivkopi_status_type AS ENUM('Bestilt', 'Startet', 'OK', 'Feilet')")
    op.execute((
        "ALTER TABLE arkivkopi ALTER COLUMN status TYPE arkivkopi_status_type USING "
        "status::text::arkivkopi_status_type"
    ))
    op.execute("DROP TYPE arkivkopi_status_type_old")
