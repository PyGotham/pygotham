"""Sponsors package."""

from pygotham.events import get_current
from pygotham.sponsors.models import Level, Sponsor

__all__ = ('get_accepted',)


def get_accepted():
    """Get the accepted sponsors."""
    return Sponsor.query.filter(
        Sponsor.accepted == True,
        Level.event == get_current(),
    ).order_by(Level.order).all()
