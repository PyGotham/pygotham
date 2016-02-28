"""Frontend application."""

from functools import wraps
import os

from flask import g, render_template
from raven.contrib.flask import Sentry
from sqlalchemy import or_

import arrow

from pygotham import factory, filters
from pygotham.core import copilot
from pygotham.about.models import AboutPage
from pygotham.events.models import Event

__all__ = ('create_app', 'route')


def create_app(settings_override=None):
    """Return the PyGotham frontend application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    Sentry(app)

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
        return {'current_event': g.current_event}

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
