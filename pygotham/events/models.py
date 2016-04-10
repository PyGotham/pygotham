"""Events models."""

import arrow
from cached_property import cached_property
from flask import current_app
from slugify import slugify
from sqlalchemy_utils import observes
from sqlalchemy_utils.types.arrow import ArrowType

from pygotham.core import db
from pygotham.events.query import EventQuery
from pygotham.talks.models import Talk

__all__ = ('Event', 'Volunteer')


class Event(db.Model):
    """Event."""

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    slug = db.Column(db.String(75), unique=True, nullable=True)

    # Event dates
    begins = db.Column(db.Date)
    ends = db.Column(db.Date)

    # Fields to control when the event is active
    active = db.Column(db.Boolean, nullable=False)
    activity_begins = db.Column(ArrowType)
    activity_ends = db.Column(ArrowType)

    # Proposal window
    proposals_begin = db.Column(ArrowType)
    proposals_end = db.Column(ArrowType)

    # When to publish the talks
    talk_list_begins = db.Column(ArrowType)
    # When to publish the schedule
    talk_schedule_begins = db.Column(ArrowType)

    # Registration information
    registration_closed = db.Column(
        db.Boolean, server_default='false', nullable=False,
    )
    registration_url = db.Column(db.String(255))
    registration_begins = db.Column(ArrowType)
    registration_ends = db.Column(ArrowType)

    def __str__(self):
        """Return a printable representation."""
        return self.name

    @cached_property
    def accepted_talks(self):
        """Return the accepted :class:`~pygotham.models.Talk` list."""
        return self.talks.filter(Talk.status == 'accepted').order_by(Talk.name)

    @observes('name')
    def _create_slug(self, title):
        """Create a slug from the name of the event."""
        if not self.slug:
            self.slug = slugify(self.name)

    @property
    def dates(self):
        """Return the date(s) for the event."""
        dates = ['{:%B %d}'.format(self.begins)]
        if self.begins != self.ends:
            if self.begins.month == self.ends.month:
                format = '{:%d}'
            else:
                format = '{:%B %d}'
            dates.append(format.format(self.ends))
        return ' - '.join(dates)

    @property
    def is_call_for_proposals_active(self):
        """Return whether the call for proposals for an event is active.

        The CFP is active when the current :class:`~datetime.datetime`
        is greater than or equal to
        :attribute:`~pygotham.events.models.Event.proposals_begin` and
        less than
        :attribute:`~pygotham.events.models.Event.proposals_end`.
        """
        now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
        if not self.proposals_begin or now < self.proposals_begin.naive:
            return False
        if self.proposals_end and self.proposals_end.naive < now:
            return False

        return True

    @property
    def is_call_for_proposals_expired(self):
        """Return whether the call for proposals has expired."""
        now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
        return self.proposals_end and self.proposals_end.naive < now

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

        now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
        begins = self.registration_begins
        if not begins or now < begins.naive:
            return False
        ends = self.registration_ends
        if ends and ends.naive < now:
            return False

        return True

    @property
    def schedule_is_published(self):
        """Return whether the schedule for an event is published."""
        now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
        talk_schedule_begins = self.talk_schedule_begins
        if not talk_schedule_begins or talk_schedule_begins.naive > now:
            return False
        return True

    @property
    def talks_are_published(self):
        """Return whether the talk list for an event is published."""
        now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
        if not self.talk_list_begins or self.talk_list_begins.naive > now:
            return False
        return True


class Volunteer(db.Model):
    """Volunteer."""

    __tablename__ = 'volunteers'
    query_class = EventQuery

    id = db.Column(db.Integer, primary_key=True)

    event_id = db.Column(db.ForeignKey('events.id'))
    event = db.relationship('Event', backref='volunteers')

    user_id = db.Column(db.ForeignKey('users.id'))
    user = db.relationship('User', uselist=False)

    def __str__(self):
        """Return a printable representation."""
        return self.user.name
