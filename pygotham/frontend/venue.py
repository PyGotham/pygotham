"""Venue for PyGotham."""

from flask import Blueprint

from pygotham.frontend import direct_to_template

__all__ = ('blueprint',)

blueprint = Blueprint('venue', __name__, url_prefix='/venue')

direct_to_template(
    blueprint, '', template='venue/index.html', endpoint='index')
