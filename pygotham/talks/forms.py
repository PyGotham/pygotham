"""Talks forms."""

from flask.ext.wtf import Form
from wtforms import HiddenField
from wtforms_alchemy import model_form_factory

from pygotham.talks.models import Talk

__all__ = 'TalkSubmissionForm',

ModelForm = model_form_factory(Form)


class TalkSubmissionForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Talk` instances."""

    id = HiddenField()

    class Meta:
        model = Talk
        exclude = ('status',)
        field_args = {
            'name': {'label': 'Title'},
            'description': {'label': 'Description'},
            'level': {'label': 'Experience Level'},
            'type': {'label': 'Type'},
            'duration': {'duration': 'Duration'},
            'abstract': {'label': 'Abstract'},
            'objectives': {'label': 'Objectives'},
            'target_audience': {'label': 'Target Audience'},
            'outline': {'label': 'Outline'},
            'additional_requirements': {'label': 'Additional Requirements'},
            'recording_release': {'label': 'Recording Release'},
        }
