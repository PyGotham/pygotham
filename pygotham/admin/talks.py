"""Admin for talk-related models."""

from pygotham.admin.utils import model_view
from pygotham.talks import models

__all__ = ('CategoryModelView', 'TalkModelView', 'TalkReviewModelView')


CategoryModelView = model_view(
    models.Category,
    'Categories',
    'Talks',
    form_columns=('name', 'slug'),
)

TalkModelView = model_view(
    models.Talk,
    'Talks',
    'Talks',
    column_list=('name', 'status', 'level', 'type', 'user'),
    column_searchable_list=('name',),
)

TalkReviewModelView = model_view(
    models.Talk,
    'Review',
    'Talks',
    can_create=False,
    can_delete=False,
    column_list=('name', 'status', 'level', 'type', 'user'),
    column_searchable_list=('name',),
    edit_template='talks/review.html',
)
