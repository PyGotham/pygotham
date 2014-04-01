"""Application factory."""

from flask import Flask
from flask.ext.security import SQLAlchemyUserDatastore

from pygotham.core import db, mail, migrate, security
from pygotham.models import Role, User
from pygotham.utils import check_required_settings, register_blueprints

__all__ = 'create_app',


def create_app(package_name, package_path, settings_override=None,
               register_security_blueprints=True):
    """Return a :class:`~flask.Flask` application.

    :param package_name: application package name.
    :param package_path: application package path.
    :param settings_override: a ``dict`` of settings to override.
    :param register_security_blueprints: whether or not to register the
                                         Flask-Security blueprints.

    """

    app = Flask(package_name, instance_relative_config=True)

    app.config.from_object('pygotham.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    check_required_settings(app.config)

    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    security.init_app(
        app,
        SQLAlchemyUserDatastore(db, User, Role),
        register_blueprint=register_security_blueprints,
    )

    register_blueprints(app, package_name, package_path)

    return app
