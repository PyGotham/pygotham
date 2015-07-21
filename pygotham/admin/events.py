"""Admin for event-related models."""

import wtforms

from pygotham.admin.utils import model_view
from pygotham.events import models

__all__ = ('EventModelView',)

CATEGORY = 'Events'


EventModelView = model_view(
    models.Event,
    'Events',
    CATEGORY,
    column_list=('name', 'slug', 'begins', 'ends', 'active'),
    form_excluded_columns=(
        'about_pages',
        'announcements',
        'calls_to_action',
        'days',
        'sponsor_levels',
        'talks',
        'volunteers',
    ),
    form_overrides={
        'activity_begins': wtforms.DateTimeField,
        'activity_ends': wtforms.DateTimeField,
        'proposals_begin': wtforms.DateTimeField,
        'proposals_end': wtforms.DateTimeField,
        'registration_begins': wtforms.DateTimeField,
        'registration_ends': wtforms.DateTimeField,
        'talk_list_begins': wtforms.DateTimeField,
        'talk_schedule_begins': wtforms.DateTimeField,
    },
)

VolunteerModelView = model_view(
    models.Volunteer,
    'Volunteers',
    CATEGORY,
    column_filters=('event.slug', 'event.name'),
    column_list=('event', 'user'),
)
