"""Frontend application."""

from collections import defaultdict
from functools import wraps
import importlib
import pkgutil
import os

from flask import g, render_template, url_for
from raven.contrib.flask import Sentry
from sqlalchemy import or_

import arrow

from pygotham import factory, filters
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

    @app.context_processor
    def generate_navbar():
        """Autodiscover links that should populate the site's navbar."""
        # navbar_links is a dict of the form
        # {section_name: {link_name: link_value, ...}, ...}
        navbar_links = defaultdict(dict)

        # First, autogenerate a list based on available routes
        # Available routes are any that have a GET method and have all
        # arguments (if any) provided default values
        for rule in app.url_map.iter_rules():
            section_name = rule.endpoint.split('.')[0]
            get_allowed = 'get' in (method.lower() for method in rule.methods)
            required_args = set(rule.arguments)
            try:
                provided_args = set(rule.defaults.keys())
            except AttributeError:
                provided_args = set()
            missing_args = required_args.difference(provided_args)
            if get_allowed and not missing_args:
                rule_name = rule.endpoint.split('.')[1]
                rule_name = rule_name.replace('_', ' ').title()
                navbar_links[section_name][rule_name] = url_for(rule.endpoint)

        # Find module-specific overrides and update the routes
        for _, name, _ in pkgutil.iter_modules(__path__):
            m = importlib.import_module('{}.{}'.format(__name__, name))
            if hasattr(m, 'get_nav_links'):
                try:
                    del navbar_links[name]
                except KeyError:
                    # We need to do this before the update in case the
                    # section name has been changed
                    pass
                navbar_links.update(m.get_nav_links())

        # Exclude certain sections whose links are exposed elsewhere
        for section in ('home', 'security', 'profile'):
            try:
                del navbar_links[section]
            except KeyError:
                # This links are displayed elsewhere, so remove the sections
                # from the navbar entirely
                pass

        nav = []
        # Normalize, hoist, and sort
        for section, links in navbar_links.items():
            index_link = links.pop('Index', None) or links.pop('Home', None)
            subnav = sorted(links.items(), key=lambda item: item[0])
            if index_link:
                subnav.insert(0, ('Home', index_link))
            nav.append((section.title(), subnav))
        nav.sort(key=lambda item: item[0])
        return {'navbar': nav}

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
