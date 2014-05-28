"""Admin for news-related models."""

from pygotham.admin.utils import model_view
from pygotham.news import models

__all__ = 'AnnouncementModelView',


AnnouncementModelView = model_view(
    models.Announcement,
    'Announcements',
    'News',
    column_default_sort='published',
    column_list=('title', 'published', 'active'),
    form_columns=('title', 'content', 'active', 'published'),
)
