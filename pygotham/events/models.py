"""Events models."""

from datetime import datetime

from pygotham.core import db

__all__ = 'Event',


class Event(db.Model):

    """Event."""

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    # Event dates
    begins = db.Column(db.Date)
    ends = db.Column(db.Date)

    # Fields to control when the event is active
    active = db.Column(db.Boolean, nullable=False)
    activity_begins = db.Column(db.DateTime)
    activity_ends = db.Column(db.DateTime)

    # Proposal window
    proposals_begin = db.Column(db.DateTime)
    proposals_end = db.Column(db.DateTime)

    # Registration informatino
    registration_closed = db.Column(
        db.Boolean, server_default='false', nullable=False,
    )
    registration_url = db.Column(db.String(255))
    registration_begins = db.Column(db.DateTime)
    registration_ends = db.Column(db.DateTime)

    def __str__(self):
        """Return a printable representation."""
        return self.name

    @property
    def is_call_for_proposals_active(self):
        """Return whether the call for proposals for an event is active.

        The CFP is active when the current :class:`~datetime.datetime`
        is greater than or equal to
        :attribute:`~pygotham.events.models.Event.proposals_begin` and
        less than
        :attribute:`~pygotham.events.models.Event.proposals_end`.
        """
        now = datetime.utcnow()
        if not self.proposals_begin or now < self.proposals_begin:
            return False
        if self.proposals_end and self.proposals_end < now:
            return False

        return True

    @property
    def is_registration_active(self):
        """Return whether registration for an event is active.

        There are several pieces to the logic of whether or not an
        event's registration is active:

        - :attribute:`~pygotham.events.models.Event.registration_closed`
          must be ``False``.
        - :attribute:`~pygotham.events.models.Event.registration_url`
          must be set.
        - :attribute:`~pygotham.events.models.Event.registration_begins`
          must be earlier than the current date and time.
        - :attribute:`~pygotham.events.models.Event.registration_ends`
          must be ``None`` or later than the current date and time.

        """
        if self.registration_closed:
            return False

        if not self.registration_url:
            return False

        now = datetime.utcnow()
        if not self.registration_begins or now < self.registration_begins:
            return False
        if self.registration_ends and self.registration_ends < now:
            return False

        return True
