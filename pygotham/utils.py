"""Application helper utilities."""

import importlib
import pkgutil

from flask import Blueprint

__all__ = 'check_required_settings', 'register_blueprints',

DOES_NOT_EXIST = '!@DNE@!'  # Placeholder value to use for missing settings.
REQUIRED_SETTINGS = 'SECRET_KEY', 'SECURITY_PASSWORD_SALT'


def check_required_settings(config, keys=REQUIRED_SETTINGS):
    """Validate the presence of required settings."""
    for key in keys:
        if config.get(key, DOES_NOT_EXIST) == DOES_NOT_EXIST:
            message = 'The {} configuration settings is required.'.format(key)
            raise RuntimeError(message)


def register_blueprints(app, package_name, package_path):
    """Register all :class:`~flask.Blueprint` instances on the app."""
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('{}.{}'.format(package_name, name))
        for x in dir(m):
            item = getattr(m, x)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
