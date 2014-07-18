"""Admin for event-related models."""

import wtforms

from pygotham.admin.utils import model_view
from pygotham.events import models

__all__ = ('EventModelView',)


EventModelView = model_view(
    models.Event,
    'Events',
    column_list=('name', 'begins', 'ends', 'active'),
    form_excluded_columns=('talks,'),
    form_overrides={
        'activity_begins': wtforms.DateTimeField,
        'activity_ends': wtforms.DateTimeField,
        'proposals_begin': wtforms.DateTimeField,
        'proposals_end': wtforms.DateTimeField,
        'registration_begins': wtforms.DateTimeField,
        'registration_ends': wtforms.DateTimeField,
        'talk_list_begins': wtforms.DateTimeField,
    },
)
