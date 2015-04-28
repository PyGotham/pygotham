"""Template filters for use across apps."""

import bleach
from docutils import core
from wtforms.fields import HiddenField

__all__ = ('rst_to_html',)

_ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'dl', 'dt', 'dd', 'cite',
]


def is_hidden_field(field):
    """Return True if a field is a hidden field."""
    return isinstance(field, HiddenField)


def rst_to_html(value):
    """Return HTML generated from reStructuredText."""
    parts = core.publish_parts(source=value, writer_name='html')
    return bleach.clean(
        parts['body_pre_docinfo'] + parts['fragment'], tags=_ALLOWED_TAGS)
