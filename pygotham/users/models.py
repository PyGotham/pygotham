"""Users models."""

from flask.ext.security import RoleMixin, UserMixin

from pygotham.core import db

__all__ = 'Role', 'User',

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
