"""Schedule models.

Much of this module is derived from the work of Eldarion on the
`Symposion <https://github.com/pinax/symposion>`_ project.

Copyright (c) 2010-2014, Eldarion, Inc. and contributors
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

    * Neither the name of Eldarion, Inc. nor the names of its contributors may
      be used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from itertools import chain, tee

from cached_property import cached_property
from sqlalchemy import func

from pygotham.core import db

__all__ = ('Day', 'Room', 'Slot', 'Presentation')


def pairwise(iterable):
    """Return values from ``iterable`` two at a time.

    Recipe from
    https://docs.python.org/3/library/itertools.html#itertools-recipes.
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

rooms_slots = db.Table(
    'rooms_slots',
    db.Column('slot_id', db.Integer, db.ForeignKey('slots.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id')),
)


class Day(db.Model):

    """Day of talks."""

    __tablename__ = 'days'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    event_id = db.Column(
        db.Integer, db.ForeignKey('events.id'), nullable=False)
    event = db.relationship(
        'Event', backref=db.backref('days', lazy='dynamic'))

    def __str__(self):
        """Return a printable representation."""
        return self.date.strftime('%B %d, %Y')

    @cached_property
    def rooms(self):
        """Return the rooms for the day."""
        return Room.query.join(rooms_slots, Slot).filter(
            Slot.day == self).order_by(Room.order).all()

    def __iter__(self):
        """Iterate over the schedule for the day."""
        if not self.rooms:
            raise StopIteration

        def rowspan(start, end):
            return times.index(end) - times.index(start)

        times = sorted(set(
            chain(*[(slot.start, slot.end) for slot in self.slots])))

        slots = db.session.query(
            Slot.id,
            Slot.content_override,
            Slot.kind,
            Slot.start,
            Slot.end,
            func.count(rooms_slots.c.slot_id).label('room_count'),
            func.min(Room.order).label('order'),
        ).join(rooms_slots, Room).filter(Slot.day == self).order_by(
            func.count(rooms_slots.c.slot_id), func.min(Room.order)
        ).group_by(
            Slot.id, Slot.content_override, Slot.kind, Slot.start, Slot.end
        ).all()

        for time, next_time in pairwise(times):
            row = {'time': time, 'slots': []}
            for slot in slots:
                if slot.start == time:
                    slot.rowspan = rowspan(slot.start, slot.end)
                    slot.colspan = slot.room_count
                    if not slot.content_override:
                        slot.presentation = Presentation.query.filter(
                            Presentation.slot_id == slot.id).first()
                    row['slots'].append(slot)
            if row['slots'] or next_time is None:
                yield row


class Room(db.Model):

    """Room of talks."""

    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __str__(self):
        """Return a printable representation."""
        return self.name


class Slot(db.Model):

    """Time slot."""

    __tablename__ = 'slots'

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(
        db.Enum(
            'break', 'meal', 'keynote', 'talk', 'tutorial', name='slotkind'),
        nullable=False,
    )
    content_override = db.Column(db.Text)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)

    day_id = db.Column(db.Integer, db.ForeignKey('days.id'), nullable=False)
    day = db.relationship('Day', backref=db.backref('slots', lazy='dynamic'))

    rooms = db.relationship(
        'Room',
        secondary=rooms_slots,
        backref=db.backref('slots', lazy='dynamic'),
        order_by=Room.order,
    )

    def __str__(self):
        """Return a printable representation."""
        start = self.start.strftime('%I:%M %p')
        end = self.end.strftime('%I:%M %p')
        rooms = ', '.join(map(str, self.rooms))
        return '{} - {} on {}, {}'.format(start, end, self.day, rooms)

    @cached_property
    def duration(self):
        """Return the duration as a :class:`~datetime.timedelta`."""
        return self.end - self.start


class Presentation(db.Model):

    """Presentation of a talk."""

    __tablename__ = 'presentations'

    id = db.Column(db.Integer, primary_key=True)

    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'), nullable=False)
    slot = db.relationship(
        'Slot', backref=db.backref('presentation', uselist=False))

    talk_id = db.Column(db.Integer, db.ForeignKey('talks.id'), nullable=False)
    talk = db.relationship(
        'Talk', backref=db.backref('presentation', uselist=False))

    def __str__(self):
        """Return a printable representation."""
        return str(self.talk)

    def is_in_all_rooms(self):
        """Return whether the instance is in all rooms."""
        return self.slot.number_of_rooms == 4

    @cached_property
    def number_of_rooms(self):
        """Return the number of rooms for the instance."""
        return len(self.slot.rooms)
