"""PyGotham speakers."""

from flask import abort, Blueprint, g, render_template

from pygotham.frontend import route
from pygotham.models import User

__all__ = ('blueprint',)

blueprint = Blueprint(
    'speakers',
    __name__,
    subdomain='<event_slug>',
    url_prefix='/speakers',
)


@route(blueprint, '/profile/<int:pk>/')
def profile(pk):
    """Return the speaker profile view."""
    if not g.current_event.talks_are_published:
        abort(404)

    # TODO: Filter by event.
    user = User.query.get_or_404(pk)
    if not user.has_accepted_talks:
        abort(404)

    return render_template('speakers/profile.html', user=user)
