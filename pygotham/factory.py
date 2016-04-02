"""Application factory."""

import arrow
from flask import Flask, g
from flask_security import SQLAlchemyUserDatastore
from sqlalchemy import or_

from pygotham.core import copilot, db, mail, migrate, security
from pygotham.models import Event, Role, User
from pygotham.utils import check_required_settings, register_blueprints

__all__ = ('create_app',)


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

    copilot.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    security.init_app(
        app,
        SQLAlchemyUserDatastore(db, User, Role),
        register_blueprint=register_security_blueprints,
    )

    register_blueprints(app, package_name, package_path)

    @app.url_defaults
    def add_event_slug(endpoint, values):
        if 'event_slug' in values or not g.current_event:
            return
        if app.url_map.is_endpoint_expecting(endpoint, 'event_slug'):
            values['event_slug'] = g.current_event.slug

    @app.url_value_preprocessor
    def current_event_from_url(endpoint, values):
        if values is None:
            values = {}
        if endpoint and app.url_map.is_endpoint_expecting(endpoint, 'event_slug'):
            now = arrow.utcnow().to('America/New_York').naive
            g.current_event = Event.query.filter(
                Event.slug == values.pop('event_slug', None),
                Event.active == True,
                or_(Event.activity_begins == None, Event.activity_begins <= now),
                or_(Event.activity_ends == None, Event.activity_ends > now),
            ).order_by(Event.activity_begins).first_or_404()
        else:
            g.current_event = Event.query.first()

    @app.context_processor
    def current_event():
        return {'current_event': getattr(g, 'current_event', None)}

    return app
