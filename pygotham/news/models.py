"""News models."""

from slugify import slugify
from sqlalchemy_utils.decorators import generates
from sqlalchemy_utils.types.arrow import ArrowType

from pygotham.core import db

__all__ = 'Announcement',


class Announcement(db.Model):

    """News announcement."""

    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    active = db.Column(db.Boolean, nullable=False)
    published = db.Column(ArrowType)

    def __str__(self):
        return self.title

    @generates(slug)
    def _create_slug(self):
        return slugify(self.title)
