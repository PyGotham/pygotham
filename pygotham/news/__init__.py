"""News package."""

import arrow
from flask import current_app

from pygotham.core import db
from pygotham.news.models import Announcement, CallToAction

__all__ = ('get_active_announcements', 'get_active_call_to_action')


def get_active_announcements():
    """Get the active announcements."""
    now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive

    # TODO: Possibly display old announcements if the current event has none.
    return Announcement.query.current.filter(
        Announcement.active == True,  # NOQA
        Announcement.published < now,
    ).order_by(db.desc(Announcement.published)).all()


def get_active_call_to_action():
    """Return the active call to action."""
    now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive

    return CallToAction.query.current.filter(
        CallToAction.active == True,  # NOQA
        CallToAction.begins < now,
        db.or_(CallToAction.ends > now, CallToAction.ends == None),
    ).order_by(CallToAction.begins, db.desc(CallToAction.ends)).first()
