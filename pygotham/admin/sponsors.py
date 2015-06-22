"""Admin for sponsor-related models."""

from pygotham.admin.utils import model_view
from pygotham.sponsors import models

__all__ = ('LevelModelView', 'SponsorModelView')

CATEGORY = 'Sponsors'


LevelModelView = model_view(
    models.Level,
    'Levels',
    CATEGORY,
    column_default_sort=('order', 'name'),
    column_filters=('event',),
    column_list=('name', 'order', 'event'),
    form_columns=('name', 'description', 'cost', 'order', 'limit', 'event'),
)


SponsorModelView = model_view(
    models.Sponsor,
    'Sponsors',
    CATEGORY,
    column_filters=('level', 'accepted', 'level.event'),
    column_list=(
        'name', 'level', 'contact_name', 'contact_email', 'accepted',
        'payment_received',
    ),
    column_searchable_list=('name', 'contact_name'),
)
