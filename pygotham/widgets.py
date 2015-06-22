"""Custom form widgets."""

from wtforms.widgets import TextInput

__all__ = ('TwitterInput',)


class TwitterInput(TextInput):

    """A widget for capturing Twitter handles."""

    def __call__(self, field, **kwargs):
        """Return the input tag."""
        kwargs.setdefault('placeholder', '@')
        return super().__call__(field, **kwargs)
