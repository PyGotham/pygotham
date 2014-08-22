"""Talks models."""

from pygotham.core import db

__all__ = ('Category', 'Talk')


class Category(db.Model):

    """Talk category."""

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(75), unique=True, nullable=False)

    def __str__(self):
        """Return a printable representation."""
        return self.name


class Talk(db.Model):

    """Talk."""

    __tablename__ = 'talks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum('draft', 'submitted', 'accepted', 'rejected', name='status'),
        default='draft',
        nullable=False,
    )
    level = db.Column(
        db.Enum('novice', 'intermediate', 'advanced', name='level'),
        nullable=False,
    )
    type = db.Column(
        db.Enum('talk', 'tutorial', name='type'),
        nullable=False,
    )
    duration = db.Column(
        db.Enum(
            '30 minutes',
            '45 minutes',
            '60 minutes',
            '1/2 day',
            'full day',
            name='duration',
        ),
        nullable=False,
    )
    recording_release = db.Column(db.Boolean, nullable=True)

    abstract = db.Column(db.Text)
    additional_requirements = db.Column(db.Text)
    objectives = db.Column(db.Text)
    outline = db.Column(db.Text)
    target_audience = db.Column(db.Text)

    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False,
    )
    event = db.relationship(
        'Event', backref=db.backref('talks', lazy='dynamic'),
    )

    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship(
        'Category', backref=db.backref('talks', lazy='dynamic'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('talks', lazy='dynamic'))

    video_url = db.Column(db.String(255))

    def __str__(self):
        """Return a printable representation."""
        return self.name

    @property
    def is_accepted(self):
        """Return whether the instance is accepted."""
        return self.status == 'accepted'
