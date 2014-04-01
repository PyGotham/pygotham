"""Events package."""

from datetime import datetime

from sqlalchemy import or_

from pygotham.events.models import Event

__all__ = 'get_current',


def get_current():
    """Get the current event."""
    now = datetime.utcnow()

    return Event.query.filter(
        Event.active == True,
        or_(Event.activity_begins == None, Event.activity_begins <= now),
        or_(Event.activity_ends == None, Event.activity_ends > now),
    ).order_by(Event.activity_begins).first()
