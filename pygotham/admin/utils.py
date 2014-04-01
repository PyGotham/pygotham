from flask.ext.admin.base import MenuLink
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from pygotham.core import db

__all__ = 'menu_link', 'model_view',


class AdminModelView(ModelView):

    """Base class for all protected admin model-based views."""

    def is_accessible(self):
        return current_user.has_role('admin')


class AuthenticatedMenuLink(MenuLink):

    """Only show a link to authenticated users."""

    def is_accessible(self):
        return current_user.is_authenticated()


class NotAuthenticatedMenuLink(MenuLink):

    """Only show a link to unauthenticated users."""

    def is_accessible(self):
        return not current_user.is_authenticated()


def menu_link(name, endpoint, authenticated):
    """Return a subclass of :class:`~flask.ext.admin.base.MenuLink`.

    :param name: name of the link.
    :param endpoint: endpoint of the view for the link.
    :param authenticated: whether or not the link is available to
                          authenticated users.

    """
    type_name = '{}MenuLink'.format(name)
    spec = (
        AuthenticatedMenuLink if authenticated else NotAuthenticatedMenuLink,
    )
    cls = type(type_name, spec, {})
    return cls(name=name, endpoint=endpoint)


def model_view(model, name, category=None, **kwargs):
    """Return a subclass of :class:`~flask.ext.admin.contrib.sql.ModelView`.

    :param model: model class to associate with the view.
    :param name: name of the menu item.
    :param category: (optional) category of the menu item.
    :param \*\*kwargs: class-level attributes for the
                       :class:`~flask.ext.admin.contrib.sqla.ModelView`.

    """
    type_name = '{}ModelView'.format(model.__class__.__name__)
    cls = type(type_name, (AdminModelView,), kwargs)
    return cls(model, db.session, name, category, name.lower())
