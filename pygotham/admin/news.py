"""Admin for news-related models."""

import wtforms

from pygotham.admin.utils import model_view
from pygotham.news import models

__all__ = ('AnnouncementModelView', 'CallToActionModelView')

CATEGORY = 'News'


AnnouncementModelView = model_view(
    models.Announcement,
    'Announcements',
    CATEGORY,
    column_default_sort='published',
    column_filters=('event',),
    column_list=('title', 'published', 'active'),
    form_columns=('title', 'content', 'active', 'published'),
    form_overrides={
        'published': wtforms.DateTimeField,
    },
)

CallToActionModelView = model_view(
    models.CallToAction,
    'Calls to Action',
    CATEGORY,
    column_default_sort='begins',
    column_filters=('event',),
    column_list=('title', 'event', 'begins', 'ends', 'active'),
    form_columns=('title', 'url', 'event', 'begins', 'ends', 'active'),
    form_overrides={
        'url': wtforms.TextField,
        'begins': wtforms.DateTimeField,
        'ends': wtforms.DateTimeField,
    },
)
