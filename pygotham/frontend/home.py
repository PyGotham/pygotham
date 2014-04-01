"""The PyGotham home page."""

from flask import Blueprint, render_template

__all__ = 'blueprint',

blueprint = Blueprint(
    'home',
    __name__,
    static_folder='static',
    static_url_path='/frontend/static',
)


@blueprint.route('/')
def index():
    """Return the home page."""
    return render_template('home/index.html')
