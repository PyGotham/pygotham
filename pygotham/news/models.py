"""News models."""

from slugify import slugify
from sqlalchemy_utils import observes
from sqlalchemy_utils.types.arrow import ArrowType

from pygotham.core import db
from pygotham.events.query import EventQuery

__all__ = ('Announcement',)


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
