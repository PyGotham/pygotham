"""PyGotham registration information."""

from flask import Blueprint

from pygotham.frontend import direct_to_template

__all__ = ('blueprint',)

blueprint = Blueprint('registration', __name__, url_prefix='/registration')

direct_to_template(
    blueprint, '/information', template='registration/information.html')
