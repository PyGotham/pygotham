"""News models."""

from slugify import slugify
from sqlalchemy_utils import observes
from sqlalchemy_utils.types.arrow import ArrowType
from sqlalchemy_utils.types.url import URLType

from pygotham.core import db
from pygotham.events.query import EventQuery

__all__ = ('Announcement', 'CallToAction')


class Announcement(db.Model):

    """News announcement."""

    __tablename__ = 'announcements'
    query_class = EventQuery

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    active = db.Column(db.Boolean, nullable=False)
    published = db.Column(ArrowType)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship(
        'Event', backref=db.backref('announcements', lazy='dynamic'))

    def __str__(self):
        """Return a printable representation."""
        return self.title

    @observes('title')
    def _create_slug(self, title):
        """Create a slug from the title of the announcement."""
        self.slug = slugify(self.title)


class CallToAction(db.Model):

    """Call to action."""

    __tablename__ = 'calls_to_action'
    query_class = EventQuery

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    url = db.Column(URLType)

    active = db.Column(db.Boolean, nullable=False)
    begins = db.Column(ArrowType)
    ends = db.Column(ArrowType)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship(
        'Event', backref=db.backref('calls_to_action', lazy='dynamic'))

    def __str__(self):
        """Return a printable representation."""
        return self.title
