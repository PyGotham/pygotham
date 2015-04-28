"""Application core."""

from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ('db',)

db = SQLAlchemy()
# NOTE: It would be cleaner to simply pass in a MetaData object to SQLAlchemy.
# Flask-SQLAlchemy supports this starting with version 2.1, which is not out at
# the time of this writing.
db.metadata.naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': '%(table_name)s_%(column_0_name)s_key',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': '%(table_name)s_%(column_0_name)s_fkey',
    'pk': '%(table_name)s_pkey',
}
mail = Mail()
migrate = Migrate()
security = Security()
