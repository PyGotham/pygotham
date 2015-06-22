"""Custom form fields."""

import re

from wtforms.fields import StringField
from wtforms.validators import ValidationError

from pygotham.widgets import TwitterInput

__all__ = ('TwitterField',)

TWITTER_HANDLE_PATTERN = re.compile(r'^\w{1,15}$')


class TwitterField(StringField):

    """A field for capturing a Twitter handle."""

    widget = TwitterInput()

    def process_data(self, value):
        """Strip a leading @ on incoming data."""
        if value and value.startswith('@'):
            value = value[1:]
        self.data = value

    def pre_validate(self, form):
        """Check that the handle conforms to Twitter restrictions."""
        self.data = self.data.replace('@', '')
        if not TWITTER_HANDLE_PATTERN.match(self.data):
            raise ValidationError('Not a valid Twitter handle.')

    def _value(self):
        """Add a leading @ on outgoing data."""
        if self.data:
            return '@' + self.data
        else:
            return ''
