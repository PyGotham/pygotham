"""About PyGotham."""

from flask import Blueprint

from pygotham.frontend import direct_to_template

__all__ = 'blueprint',

blueprint = Blueprint('about', __name__, url_prefix='/about')

direct_to_template(
    blueprint,
    '/code-of-conduct',
    template='about/code-of-conduct.html',
    endpoint='code_of_conduct',
)
direct_to_template(
    blueprint,
    '/privacy-policy',
    template='about/privacy-policy.html',
    endpoint='privacy_policy',
)
