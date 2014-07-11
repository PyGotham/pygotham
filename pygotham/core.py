"""Application core."""

from flask.ext.mail import Mail
from flask.ext.migrate import Migrate
from flask.ext.security import Security
from flask.ext.sqlalchemy import SQLAlchemy

__all__ = ('db',)

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
security = Security()
