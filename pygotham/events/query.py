from flask import g
from flask_sqlalchemy import BaseQuery


__all__ = ('EventQuery',)


class EventQuery(BaseQuery):
    """Provides a query filtered by default by the current event.

    Interface example: Model.query.current.filter(...)
    """
    @property
    def current(self):
        # Circular import
        return self.filter_by(event=g.current_event)
