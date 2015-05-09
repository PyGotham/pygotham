"""Events forms."""

from flask_wtf import Form
from wtforms_alchemy import model_form_factory

from pygotham.models import Event

__all__ = ('EventForm',)

ModelForm = model_form_factory(Form)


class EventForm(ModelForm):

    """Form for creating :class:`~pygotham.models.Event` instances."""

    class Meta:
        model = Event
        only = ('name', 'slug', 'begins', 'ends', 'proposals_begin', 'active')
