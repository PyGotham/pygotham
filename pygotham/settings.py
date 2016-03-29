"""Application settings."""

from os import environ as env

from pygotham.utils import DOES_NOT_EXIST


def bool_(key, default):
    """Return an environment setting represented as a boolean."""
    return env.get(key, str(default)).lower() == 'true'


DEBUG = bool_('DEBUG', False)
SECRET_KEY = env.get('SECRET_KEY', DOES_NOT_EXIST)
SERVER_NAME = env.get('SERVER_NAME')

GOOGLE_ANALYTICS_PROFILE_ID = env.get('GOOGLE_ANALYTICS_PROFILE_ID')

# Flask-Assets
ASSETS_DEBUG = bool_('ASSETS_DEBUG', False)

# Flask-Foundation
FOUNDATION_HTML5_SHIM = bool_('FOUNDATION_HTML5_SHIM', True)
FOUNDATION_USE_CDN = bool_('FOUNDATION_USE_CDN', True)
FOUNDATION_USE_MINIFIED = bool_('FOUNDATION_USE_MINIFIED', True)

# Flask-Mail
MAIL_SERVER = env.get('MAIL_SERVER', 'localhost')
MAIL_PORT = int(env.get('MAIL_PORT', 25))
MAIL_USERNAME = env.get('MAIL_USERNAME')
MAIL_PASSWORD = env.get('MAIL_PASSWORD')
MAIL_USE_SSL = bool_('MAIL_USE_SSL', True)
MAIL_USE_TLS = bool_('MAIL_USE_TLS', True)
MAIL_DEBUG = bool_('MAIL_DEBUG', False)
MAIL_DEFAULT_SENDER = env.get('MAIL_DEFAULT_SENDER')

# Flask-Security
SECURITY_CHANGEABLE = True
SECURITY_DEFAULT_REMEMBER_ME = True
SECURITY_EMAIL_SENDER = MAIL_DEFAULT_SENDER
SECURITY_EMAIL_SUBJECT_REGISTER = 'Welcome to PyGotham'
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = env.get('SECURITY_PASSWORD_SALT', DOES_NOT_EXIST)
SECURITY_POST_REGISTER_VIEW = 'profile.settings'
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = bool_('SECURITY_SEND_REGISTER_EMAIL', True)
SECURITY_SUBDOMAIN = '<event_slug>'
SECURITY_TRACKABLE = True

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = env.get('DATABASE_URL')

del bool_
del env
del DOES_NOT_EXIST
