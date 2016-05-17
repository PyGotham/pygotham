"""Add reviewer role

Revision ID: 90f1af83d9b6
Revises: 5d619660cfa7
Create Date: 2016-05-17 02:16:30.097950

"""

# revision identifiers, used by Alembic.
revision = '90f1af83d9b6'
down_revision = '5d619660cfa7'

from alembic import op


def upgrade():
    """Add reviewer role."""
    op.execute("INSERT INTO roles (name) VALUES ('reviewer');")


def downgrade():
    """Remove reviewer role and dependencies."""
    op.execute(
        "DELETE FROM roles_users WHERE role_id in ("
        "SELECT id FROM roles WHERE name='reviewer');"
    )
    op.execute("DELETE FROM roles WHERE name='reviewer';")
