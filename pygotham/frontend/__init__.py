"""Frontend application."""

from collections import defaultdict
from functools import wraps
import importlib
import pkgutil
import os

from flask import render_template, url_for
from flask.ext.assets import Bundle, Environment
from flask.ext.foundation import Foundation
from raven.contrib.flask import Sentry

from pygotham import factory, filters
from pygotham.events import get_current as get_current_event

__all__ = ('create_app', 'route')


def create_app(settings_override=None):
    """Return the PyGotham frontend application.

    :param settings_override: a ``dict`` of settings to override.

    """
    app = factory.create_app(__name__, __path__, settings_override)

    assets = Environment(app)
    Foundation(app)
    Sentry(app)

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
                navbar_links[section_name][rule_name] = url_for(rule.endpoint)

        # Find module-specific overrides and update the routes
        for _, name, _ in pkgutil.iter_modules(__path__):
            m = importlib.import_module('{}.{}'.format(__name__, name))
            if hasattr(m, 'get_nav_links'):
                for section, override_links in m.get_nav_links().items():
                    navbar_links[section].update(override_links)

        # Exclude certain sections whose links are exposed elsewhere
        for section in ('home', 'security', 'profile'):
            try:
                del navbar_links[section]
            except KeyError:
                pass

        nav = []
        # Normalize, hoist, and sort
        for section, links in navbar_links.items():
            index_link = links.pop('index', None) or links.pop('home', None)
            subnav = [(title.replace('_', ' ').title(), link) for
                      title, link in links.items()]
            subnav.sort(key=lambda item: item[0])
            if index_link:
                subnav.insert(0, ('Home', index_link))
            nav.append((section.title(), subnav))
        nav.sort(key=lambda item: item[0])
        return {'navbar': nav}

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
