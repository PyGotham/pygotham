"""Admin for talk-related models."""

from flask_admin import actions
from flask.ext.admin.contrib.sqla import ModelView

from pygotham.admin.utils import model_view
from pygotham.core import db
from pygotham.talks import models

__all__ = ('CategoryModelView', 'talk_model_view', 'TalkReviewModelView')

CATEGORY = 'Talks'


class TalkModelView(ModelView, actions.ActionsMixin):
    """Admin view for :class:`~pygotham.models.Talk`."""

    column_default_sort = 'id'
    column_filters = (
        'status', 'duration', 'level', 'event.slug', 'event.name')
    column_list = ('name', 'status', 'duration', 'level', 'type', 'user')
    column_searchable_list = ('name',)
    form_excluded_columns = ('presentation',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_actions()

    @actions.action(
        'accept', 'Accept', 'Are you sure you want to accept selected models?')
    def approve(self, talks):
        for pk in talks:
            talk = models.Talk.query.get(pk)
            talk.status = 'accepted'
        self.session.commit()

    @actions.action(
        'reject', 'Reject', 'Are you sure you want to reject selected models?')
    def reject(self, talks):
        for pk in talks:
            talk = models.Talk.query.get(pk)
            talk.status = 'rejected'
        self.session.commit()


CategoryModelView = model_view(
    models.Category,
    'Categories',
    CATEGORY,
    form_columns=('name', 'slug'),
)

DurationModelView = model_view(
    models.Duration,
    'Durations',
    CATEGORY,
)


talk_model_view = TalkModelView(
    models.Talk, db.session, 'Talks', CATEGORY, 'talks')


TalkReviewModelView = model_view(
    models.Talk,
    'Review',
    CATEGORY,
    can_create=False,
    can_delete=False,
    column_default_sort='id',
    column_filters=('event.slug', 'event.name'),
    column_list=('name', 'status', 'level', 'type', 'user'),
    column_searchable_list=('name',),
    edit_template='talks/review.html',
)
