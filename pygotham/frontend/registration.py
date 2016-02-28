"""PyGotham registration information."""

from flask import Blueprint, g, url_for

from pygotham.frontend import direct_to_template

__all__ = ('blueprint', 'get_nav_links')

blueprint = Blueprint(
    'registration',
    __name__,
    url_prefix='/<event_slug>/registration',
)

direct_to_template(
    blueprint,
    '/information/',
    template='registration/information.html',
    navbar_kwargs={'path': ('Registration', 'Information')},
)


def get_nav_links():
    """Return registration-related menu items."""
    links = {
        'Information': url_for('registration.information'),
    }
    if g.current_event.is_registration_active:
        links['Register'] = g.current_event.registration_url
    return {'Registration': links}
