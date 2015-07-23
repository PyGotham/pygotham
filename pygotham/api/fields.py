"""Fieldsets rendered via Flask-Restful."""

from flask_restful import fields


class MockField(fields.Raw):

    """Return whatever is passed into the initializer."""

    def __init__(self, mock_value, **kwargs):
        """Store the mock value provided and pass the rest to super()."""
        self.mock_value = mock_value
        super().__init__(**kwargs)

    def output(self, key, obj):
        """Return the mock value provided."""
        return self.mock_value


class AttrField(fields.Raw):

    """Return the value of an attribute of obj."""

    def __init__(self, attr, post_processor=None, **kwargs):
        """Store the attr name provided and pass the rest to super()."""
        self.attr = attr
        self.post_processor = post_processor
        super().__init__(**kwargs)

    def output(self, key, obj):
        """Return the value of attr on obj."""
        parts = self.attr.split('.')
        attr = parts.pop(0)
        value = getattr(obj, attr)
        for part in parts:
            if value is None:
                return None
            value = getattr(value, part)
        # HACK: post_processor shouldn't be needed. We should use an
        # approach similar to fields.Nested here.
        if self.post_processor is not None:
            return self.post_processor(value)
        return value

event_fields = {
    'id': fields.Integer,
    'begins': fields.DateTime('iso8601'),
    'ends': fields.DateTime('iso8601'),
    'name': fields.String,
    'registration_url': fields.String,
    'slug': fields.String,
}

user_fields = {
    'id': fields.Integer,
    'bio': fields.String,
    'email': MockField('<redacted>'),
    'name': fields.String,
    'picture_url': MockField(None),
    'twitter_id': AttrField('twitter_handle'),
}

talk_fields = {
    'id': fields.Integer,
    'conf_key': AttrField('event_id'),
    'conf_url': MockField('https://pygotham.org/2015/'),
    'description': fields.String,
    'duration': AttrField('duration.duration'),
    'language': MockField('English'),
    # TODO: How should this be generated?
    'summary': AttrField('description'),
    'room': AttrField(
        'presentation.slot.rooms',
        lambda rooms: ' & '.join(room.name for room in rooms),
    ),
    'room_alias': AttrField(
        'presentation.slot.rooms',
        lambda rooms: ' & '.join(room.name for room in rooms),
    ),
    # NOTE: This should probably be nested instead of inlined this way.
    'start': AttrField(
        'presentation.slot',
        lambda slot: '{:%Y-%m-%d}T{:%H:%M:%S}'.format(slot.day.date, slot.start),
    ),
    # TODO: this should be based on the recording release
    'priority': MockField(9),
    # FIXME: What version are the talks to be licensed under?
    'license': MockField('Creative Commons'),
    'tags': MockField([]),
    'title': AttrField('name'),
    'user': fields.Nested(user_fields),
}
