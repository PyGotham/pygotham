"""Admin for user-related models."""

from pygotham.admin.utils import model_view
from pygotham.users import models

__all__ = 'RoleModelView', 'UserModelView'


RoleModelView = model_view(models.Role, 'Roles', 'Users')

UserModelView = model_view(
    models.User,
    'Users',
    'Users',
    column_list=('name', 'email', 'active'),
    column_searchable_list=('name', 'email'),
    form_columns=('name', 'email', 'active', 'roles'),
)
