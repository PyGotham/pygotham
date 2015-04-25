"""Sponsors forms."""

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Email
from wtforms_alchemy import model_form_factory

from pygotham.models import Level, Sponsor

__all__ = ('SponsorApplicationForm', 'SponsorEditForm')

ModelForm = model_form_factory(Form)


class SponsorApplicationForm(ModelForm):

    """Form for creating :class:`~pygotham.models.Sponsor` instances."""

    # TODO: Filter by event.
    level = QuerySelectField(query_factory=Level.query.all)

    class Meta:
        model = Sponsor
        only = ('name', 'contact_name', 'contact_email')
        field_args = {
            'name': {'label': 'Sponsor Name'},
            'contact_name': {'label': 'Contact Name'},
            'contact_email': {
                'label': 'Contact Email',
                'validators': (Email(),),
            },
        }


class SponsorEditForm(ModelForm):

    """Form for editing :class:`~pygotham.models.Sponsor` instances.

    The difference between this and
    :class:`~pygotham.forms.SponsorApplicationForm` is that this form
    does not allow ``level`` to be edited.
    """

    class Meta:
        model = Sponsor
        only = ('name', 'contact_name', 'contact_email')
        field_args = {
            'name': {'label': 'Sponsor Name'},
            'contact_name': {'label': 'Contact Name'},
            'contact_email': {
                'label': 'Contact Email',
                'validators': (Email(),),
            },
        }
