"""Custom query for models that can be filtered by the current event."""

from flask import g
from flask_sqlalchemy import BaseQuery


__all__ = ('EventQuery',)


class EventQuery(BaseQuery):
    """Provide a query class filtered by the current event.

    Interface example: Model.query.current.filter(...)
    """

    @property
    def current(self):
        """Return a query filtered by the current event."""
        # Circular import
        return self.filter_by(event=g.current_event)
