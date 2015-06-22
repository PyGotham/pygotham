"""Users forms."""

from flask_wtf import Form
from wtforms.fields import HiddenField
from wtforms.validators import Email, Optional
from wtforms_alchemy import Unique, model_form_factory

from pygotham.fields import TwitterField
from pygotham.models import User

__all__ = ('ProfileForm',)

ModelForm = model_form_factory(Form)


class ProfileForm(ModelForm):

    """Form for editing :class:`~pygotham.models.User` instances."""

    id = HiddenField()
    twitter_handle = TwitterField(
        'Twitter', validators=(Unique(User.twitter_handle), Optional()))

    class Meta:
        model = User
        only = ('name', 'email', 'bio')
        field_args = {
            'name': {'label': 'Name'},
            'email': {
                'label': 'Email',
                'validators': (Email(), Unique(User.email)),
            },
            'bio': {'label': 'Biography'},
        }
