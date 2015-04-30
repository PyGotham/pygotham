from flask_sqlalchemy import BaseQuery


__all__ = ('EventQuery',)


class EventQuery(BaseQuery):
    """Provides a query filtered by default by the current event.

    Interface example: Model.query.current.filter(...)
    """
    @property
    def current(self):
        # Circular import
        from pygotham.events import get_current
        return self.filter_by(event=get_current())
