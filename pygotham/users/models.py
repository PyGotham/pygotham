"""Users models."""

import random
import string

from cached_property import cached_property
from flask_security import RoleMixin, UserMixin, recoverable
from sqlalchemy import event

from pygotham.core import db
from pygotham.talks.models import Talk

__all__ = ('Role', 'User')

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
)


class Role(db.Model, RoleMixin):

    """User role."""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        """Return a printable representation."""
        return self.name

    def __eq__(self, other):
        return self.name == other or self.name == getattr(other, 'name', None)

    def __hash__(self):
        return id(self)

    def __ne__(self, other):
        return self.name != other and self.name != getattr(other, 'name', None)


class User(db.Model, UserMixin):

    """User."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), info={'label': 'Name'})
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(130))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    registered_at = db.Column(db.DateTime)

    bio = db.Column(db.Text)

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )

    def __str__(self):
        """Return a printable representation."""
        return self.name or self.email

    def __eq__(self, other):
        return self.id == getattr(other, 'id', None)

    def __hash__(self):
        return id(self)

    def __ne__(self, other):
        return self.id != getattr(other, 'id', None)

    @cached_property
    def accepted_talks(self):
        """Return the user's accepted talks."""
        return Talk.query.current.filter(
            Talk.status == 'accepted', Talk.user == self).order_by(Talk.name)

    @cached_property
    def has_accepted_talks(self):
        """Return whether the user has accepted talks."""
        return self.accepted_talks.count() > 0


@event.listens_for(User, 'before_insert')
def user_create_send_password_reset(mapper, connection, target):
    """Send a password reset to users created without an email."""
    if not target.password:
        target.password = ''.join(
            random.choice(string.printable) for _ in range(20))
        recoverable.send_reset_password_instructions(target)
