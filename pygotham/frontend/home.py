"""The PyGotham home page."""

from flask import Blueprint, render_template

from pygotham.news import get_active_announcements, get_active_call_to_action
from pygotham.sponsors import get_accepted

__all__ = ('blueprint',)

blueprint = Blueprint(
    'home',
    __name__,
    static_folder='static',
    static_url_path='/frontend/static',
    subdomain='<event_slug>',
)


@blueprint.route('/')
def index():
    """Return the home page."""
    announcements = get_active_announcements()
    cta = get_active_call_to_action()
    sponsors = get_accepted()
    return render_template(
        'home/index.html',
        announcements=announcements,
        cta=cta,
        sponsors=sponsors,
    )
