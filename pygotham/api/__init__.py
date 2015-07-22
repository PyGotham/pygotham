"""PyGotham data API."""

from pygotham import factory

__all__ = ('create_app',)


def create_app(settings_override=None):
    """Return the PyGotham API application.

    :param settings_override: a ``dict`` of settings to override.
    """
    app = factory.create_app(__name__, __path__, settings_override)
    return app
