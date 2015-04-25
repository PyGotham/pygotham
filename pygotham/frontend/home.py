"""The PyGotham home page."""

from flask import Blueprint, render_template

from pygotham.news import get_active
from pygotham.sponsors import get_accepted

__all__ = ('blueprint',)

blueprint = Blueprint(
    'home',
    __name__,
    static_folder='static',
    static_url_path='/frontend/static',
)


@blueprint.route('/')
def index():
    """Return the home page."""
    # TODO: Filter by event.
    announcements = get_active()
    # TODO: Filter by event.
    sponsors = get_accepted()
    return render_template(
        'home/index.html', announcements=announcements, sponsors=sponsors)
