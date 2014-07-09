"""Admin application."""

import importlib
import pkgutil

from flask.ext.admin import Admin
from flask.ext.admin.base import AdminIndexView, MenuLink
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user

from pygotham import factory, filters

__all__ = 'create_app',


class HomeView(AdminIndexView):

    """Only show the admin to authenticated admin users."""

    def is_accessible(self):
        return current_user.has_role('admin')


def create_app(settings_override=None):
    """Return the PyGotham admin application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    app.jinja_env.filters['rst'] = filters.rst_to_html

    # Because the admin is being wrapped inside an app, the url needs to
    # be overridden to use / instead of the default of /admin/. One of
    # the side effects of doing this is that the static assets won't
    # serve correctly without overriding static_url_path as well.
    admin = Admin(
        app, name='PyGotham',
        static_url_path='/admin',
        index_view=HomeView(endpoint='', url='/'),
    )

    # Iterate through all the modules of the current package. For each
    # module, check the public API for any instances of types that can
    # be added to the Flask-Admin menu and register them.
    for _, name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module('{}.{}'.format(__name__, name))
        for attr in dir(module):
            view = getattr(module, attr)
            if isinstance(view, ModelView):
                admin.add_view(view)
            elif isinstance(view, MenuLink):
                admin.add_link(view)

    return app
