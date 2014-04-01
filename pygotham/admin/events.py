"""Admin for event-related models."""

from pygotham.admin.utils import model_view
from pygotham.events import models

__all__ = 'EventModelView',


EventModelView = model_view(
    models.Event,
    'Events',
    column_list=('name', 'begins', 'ends', 'active'),
    form_excluded_columns=('talks,'),
)
