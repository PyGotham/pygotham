"""Talks forms."""

from flask.ext.wtf import Form
from wtforms import HiddenField
from wtforms.validators import Optional
from wtforms_alchemy import model_form_factory

from pygotham.talks.models import Talk

__all__ = 'TalkSubmissionForm',

ModelForm = model_form_factory(Form)


class TalkSubmissionForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Talk` instances."""

    class Meta:
        model = Talk
        exclude = ('status',)
        field_args = {
            'name': {'label': 'Title'},
            'description': {'label': 'Please include a brief summary of the talk as it should appear on the site'},
            'level': {'label': 'Experience Level'},
            'type': {'label': 'Type'},
            'duration': {'label': 'Duration'},
            'abstract': {'label': 'Please give a more detailed description of the talk'},
            'objectives': {'label': 'Objectives'},
            'target_audience': {'label': 'Target Audience'},
            'outline': {'label': 'This outline should cover the sections and key points of the talk (think table of contents'},
            'additional_requirements': {'label': 'Additional Requirements'},
            'recording_release': {
                'label': 'Recording Release',
                'validators': (Optional(),),
            },
        }
