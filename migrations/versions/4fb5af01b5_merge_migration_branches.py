"""Merge migration branches

Revision ID: 4fb5af01b5
Revises: ('177a65486a0', '4c236d4eac4')
Create Date: 2015-04-29 22:19:38.477770

"""

# revision identifiers, used by Alembic.
revision = '4fb5af01b5'
down_revision = ('177a65486a0', '4c236d4eac4')

from alembic import op
import sqlalchemy as sa


def upgrade():
    pass


def downgrade():
    pass
