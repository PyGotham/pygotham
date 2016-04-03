"""Frontend application."""

from functools import wraps
import os

from flask import render_template
from raven.contrib.flask import Sentry

from pygotham import factory, filters
from pygotham.core import copilot
from pygotham.models import AboutPage

__all__ = ('create_app', 'route')


def create_app(settings_override=None):
    """Return the PyGotham frontend application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    Sentry(app)

    @app.before_request
    def register_about_page_navbar_links():
        """Generate all about page titles and URLs for use in the navbar."""
        for page in AboutPage.query.current.filter_by(active=True):
            copilot.register_entry({
                'path': (page.navbar_section, page.title),
                'endpoint': 'about.rst_content',
                'url_for_kwargs': {'slug': page.slug},
            })

    app.jinja_env.filters['clean_url'] = filters.clean_url
    app.jinja_env.filters['is_hidden_field'] = filters.is_hidden_field
    app.jinja_env.filters['rst'] = filters.rst_to_html
    app.jinja_env.filters['time_zone'] = filters.time_zone

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
