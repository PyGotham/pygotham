"""Sponsors package."""

from pygotham.sponsors.models import Level, Sponsor

__all__ = ('get_accepted',)


def get_accepted():
    """Get the accepted sponsors."""
    return Sponsor.query.current.filter(
        Sponsor.accepted == True).join(Level).order_by(Level.order).all()
