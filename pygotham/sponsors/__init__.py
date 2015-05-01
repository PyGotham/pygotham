"""Sponsors package."""

from flask import g

from pygotham.sponsors.models import Level, Sponsor

__all__ = ('get_accepted',)


def get_accepted():
    """Get the accepted sponsors."""
    return Sponsor.query.filter(
        Sponsor.accepted == True,
        Level.event == g.current_event,
    ).order_by(Level.order).all()
