"""Template filters for use across apps."""

from urllib.parse import urlparse

import bleach
from docutils import core
from flask import current_app
from wtforms.fields import HiddenField

__all__ = ('rst_to_html',)

_ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'dl', 'dt', 'dd', 'cite',
]
_ALLOWED_ATTRIBUTES = bleach.ALLOWED_ATTRIBUTES.copy()
_ALLOWED_ATTRIBUTES['img'] = ['alt', 'height', 'src', 'width']


def clean_url(value):
    """Return a URL without the schema and query string."""
    parts = urlparse(value)
    return parts.netloc + (parts.path if parts.path != '/' else '')


def is_hidden_field(field):
    """Return True if a field is a hidden field."""
    return isinstance(field, HiddenField)


def rst_to_html(value, extra_tags=None):
    """Return HTML generated from reStructuredText."""
    parts = core.publish_parts(
        source=value,
        writer_name='html',
        settings_overrides={'doctitle_xform': False})

    # Strip disallowed tags so the output doesn't appear broken.
    return bleach.clean(
        parts['body_pre_docinfo'] + parts['fragment'],
        tags=_ALLOWED_TAGS + (extra_tags or []),
        attributes=_ALLOWED_ATTRIBUTES,
        strip=True,
    )


def time_zone(value):
    """Return the local time zone for the given datetime."""
    tz = value.to(current_app.config['TIME_ZONE'])
    return tz.tzname()
