"""Admin for user-related models."""

from wtforms.validators import Optional
from wtforms_alchemy import Unique

from pygotham.admin.utils import model_view
from pygotham.fields import TwitterField
from pygotham.users import models

__all__ = ('RoleModelView', 'UserModelView')


RoleModelView = model_view(models.Role, 'Roles', 'Users')

UserModelView = model_view(
    models.User,
    'Users',
    'Users',
    column_list=('name', 'email', 'twitter_handle', 'active'),
    column_searchable_list=('name', 'email'),
    form_args={
        'twitter_handle': {
            'validators': [Unique(models.User.twitter_handle), Optional()],
        },
    },
    form_columns=('name', 'email', 'twitter_handle', 'bio', 'active', 'roles'),
    form_overrides={'twitter_handle': TwitterField},
)
