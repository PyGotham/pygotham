"""PyGotha speakers."""

from flask import abort, Blueprint, render_template

from pygotham.events import get_current as get_current_event
from pygotham.frontend import route
from pygotham.models import User

__all__ = ('blueprint',)

blueprint = Blueprint('speakers', __name__, url_prefix='/speakers')


@route(blueprint, '/profile/<int:pk>')
def profile(pk):
    """Return the speaker profile view."""
    event = get_current_event()
    if not event.talks_are_published:
        abort(404)

    # TODO: Filter by event.
    user = User.query.get_or_404(pk)
    if not user.has_accepted_talks:
        abort(404)

    return render_template('speakers/profile.html', user=user)
