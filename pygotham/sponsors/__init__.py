"""Sponsors package."""

from pygotham.sponsors.models import Level, Sponsor

__all__ = ('get_accepted',)


def get_accepted():
    """Get the accepted sponsors."""
    # TODO: Filter by event.
    return Sponsor.query.filter(
        Sponsor.accepted == True).join(Level).order_by(Level.order).all()
