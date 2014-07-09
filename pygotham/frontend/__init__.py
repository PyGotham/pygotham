"""Frontend application."""

from functools import wraps
import os

from flask import render_template
from flask.ext.assets import Bundle, Environment
from flask.ext.foundation import Foundation

from pygotham import factory, filters
from pygotham.events import get_current as get_current_event

__all__ = 'create_app', 'route'


def create_app(settings_override=None):
    """Return the PyGotham frontend application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    assets = Environment(app)
    Foundation(app)

    css_screen = Bundle(
        'css/screen.css',
        filters='cssmin',
        output='gen/css/screen.min.css',
    )
    css_print = Bundle(
        'css/print.css',
        filters='cssmin',
        output='gen/css/print.min.css',
    )

    css_foundation = Bundle(
        'foundation/css/normalize.css',
        'foundation/css/foundation.css',
        'foundation/css/app.css',
        filters='cssmin',
        output='gen/css/foundation.min.css',
    )

    js_foundation = Bundle(
        'foundation/js/foundation.min.js',
        'foundation/js/app.js',
        filters='jsmin',
        output='gen/js/foundation.min.js',
    )

    assets.register('css_screen', css_screen)
    assets.register('css_print', css_print)
    assets.register('css_foundation', css_foundation)
    assets.register('js_foundation', js_foundation)

    @app.context_processor
    def current_event():
        return {'current_event': get_current_event()}

    app.jinja_env.filters['rst'] = filters.rst_to_html

    if not app.debug:
        for e in (404, 500):
            app.errorhandler(e)(handle_error)

    return app


def direct_to_template(blueprint, rule, template, **kwargs):
    """Return a view rendered directly from a template."""
    def f(template, **kwargs):
        return render_template(template, **kwargs)

    endpoint = kwargs.pop('endpoint', None)
    if not endpoint:
        endpoint = os.path.basename(template).split('.')[0]

    blueprint.add_url_rule(
        rule,
        endpoint=endpoint,
        view_func=f,
        defaults={'template': template},
        **kwargs)


def handle_error(error):
    """Return the rendered error template."""
    return render_template('errors/{}.html'.format(error.code)), error.code


def route(blueprint, *args, **kwargs):
    """Return a route."""
    def decorator(f):
        @blueprint.route(*args, **kwargs)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return f
    return decorator
