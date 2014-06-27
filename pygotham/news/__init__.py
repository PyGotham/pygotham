"""News package."""

import arrow

from pygotham.core import db
from pygotham.news.models import Announcement

__all__ = 'get_active',


def get_active():
    """Get the active announcements."""
    now = arrow.utcnow().to('America/New_York')

    return Announcement.query.filter(
        Announcement.active == True,
        Announcement.published < now,
    ).order_by(db.desc(Announcement.published)).all()
