"""Add about_pages table

Revision ID: 4c236d4eac4
Revises: 55a2c1bad7
Create Date: 2015-04-22 23:45:51.210213

"""

# revision identifiers, used by Alembic.
revision = '4c236d4eac4'
down_revision = '55a2c1bad7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'about_pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('navbar_section', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint(
            'navbar_section', 'slug', 'event_id',
            name='ix_about_pages_navbar_section_slug_event_id',
        ),
    )


def downgrade():
    op.drop_table('about_pages')
