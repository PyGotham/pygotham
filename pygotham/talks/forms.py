"""Talks forms."""

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Optional
from wtforms_alchemy import model_form_factory

from pygotham.talks.models import Duration, Talk

__all__ = ('TalkSubmissionForm',)

ModelForm = model_form_factory(Form)


def duration_query_factory():
    """Return available :class:`~pygotha.models.Duration` instances."""
    return Duration.query.filter(Duration.inactive == False)


class TalkSubmissionForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Talk` instances."""

    class Meta:
        model = Talk
        exclude = (
            'abstract',
            'objectives',
            'outline',
            'status',
            'target_audience',
            'type',
        )
        field_args = {
            'name': {'label': 'Title'},
            'description': {
                'label': 'Description',
                'description': (
                    'If your talk is accepted this will be made public. '
                    'Should be one paragraph.'
                ),
            },
            'level': {'label': 'Experience Level'},
            'duration': {'label': 'Duration'},
            'additional_requirements': {'label': 'Additional Requirements'},
            'recording_release': {
                'label': 'Recording Release',
                'validators': (Optional(),),
            },
        }

    duration = QuerySelectField(query_factory=duration_query_factory)
