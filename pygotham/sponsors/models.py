"""Sponsors models."""

from pygotham.core import db

_all__ = 'Level', 'Sponsor'


class Level(db.Model):

    """Sponsorship level."""

    __tablename__ = 'sponsor_levels'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

    def __str__(self):
        return self.name


class Sponsor(db.Model):

    """Sponsor."""

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    accepted = db.Column(db.Boolean)
    level_id = db.Column(
        db.Integer, db.ForeignKey('sponsor_levels.id'), nullable=False,
    )
    level = db.relationship(
        'Level', backref=db.backref('sponsors', lazy='dynamic'),
    )

    applicant_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False,
    )
    applicant = db.relationship('User')
