"""Fieldsets rendered via Flask-Restful."""

from pygotham.models import Event, Level, Sponsor, Talk, User

from .core import marshmallow

__all__ = ('EventSchema', 'SponsorSchema', 'TalkSchema', 'UserSchema')


class EventSchema(marshmallow.Schema):
    """Serialization rules for Event objects."""

    class Meta:
        model = Event
        fields = ('id', 'begins', 'ends', 'name', 'registration_url', 'slug')


class UserSchema(marshmallow.Schema):
    """Serialization rules for User objects."""

    class Meta:
        model = User
        additional = ('id', 'bio', 'name')

    email = marshmallow.Function(lambda user: '<redacted>')
    picture_url = marshmallow.Function(lambda user: None)
    twitter_id = marshmallow.Function(lambda user: user.twitter_handle)


class LevelSchema(marshmallow.Schema):
    """Serialization rules for sponsorship Level objects."""

    class Meta:
        model = Level
        # The highest sponsorship tiers have the lowest order.
        # TODO: Have a real place to put documentation like the comment
        # above.
        additional = ('name', 'order')


class SponsorSchema(marshmallow.Schema):
    """Serialization rules for Sponsor objects."""

    class Meta:
        model = Sponsor
        additional = ('description', 'logo', 'name', 'url')

    level = marshmallow.Nested(LevelSchema)


class TalkSchema(marshmallow.Schema):
    """Serialization rules for Talk objects."""

    class Meta:
        model = Talk
        additional = ('id', 'description')

    conf_key = marshmallow.Function(lambda talk: talk.id)
    duration = marshmallow.Function(lambda talk: talk.duration.duration)
    language = marshmallow.Function(lambda talk: 'English')
    # FIXME: What version are the talks to be licensed under?
    license = marshmallow.Function(lambda talk: 'Creative Commons')
    priority = marshmallow.Method('get_recording_priority')
    released = marshmallow.Function(lambda talk: talk.recording_release)
    # TODO: Replace this with a nested SlotSchema.
    room = marshmallow.Method('get_room')
    room_alias = marshmallow.Method('get_room')
    # TODO: Replace this with a nested SlotSchema.
    start = marshmallow.Method('get_start_time')
    summary = marshmallow.Function(lambda talk: talk.description)
    tags = marshmallow.Function(lambda talk: [])
    title = marshmallow.Function(lambda talk: talk.name)
    user = marshmallow.Nested(UserSchema)

    def get_recording_priority(self, talk):
        """Get the numerical recording priority for a talk.

        Args:
            talk (pygotham.talks.models.Talk): The talk.
        """
        # HACK: Generate the recording priority based on recording
        # release. We probably won't have any 5s, but this is about as
        # correct as the mapping can be at the moment.
        priority_mapping = {True: 9, False: 0, None: 5}
        return priority_mapping[talk.recording_release]

    def get_room(self, talk):
        """Get a one line representation of a talk's scheduled room.

        In most cases, talks are in one room. Occasionally, however, a
        talk may span multiple rooms. When that happens, return a
        descriptive string combining room names.

        Args:
            talk (pygotham.talks.models.Talk): The talk.
        """
        return ' & '.join(room.name for room in talk.presentation.slot.rooms)

    def get_start_time(self, talk):
        """Return an IOS8601 formatted start time.

        Args:
            talk (pygotham.talks.models.Talk): The talk.
        """
        return '{:%Y-%m-%d}T{:%H:%M:%S}'.format(
            talk.presentation.slot.day.date,
            talk.presentation.slot.start,
        )
