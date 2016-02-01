"""Event-related management commands."""

import sys

import arrow
from flask_script import Command, prompt, prompt_bool
from werkzeug.datastructures import MultiDict

from pygotham.core import db
from pygotham.forms import EventForm
from pygotham.models import Event


class CreateEvent(Command):
    """Management command to create an :class:`~pygotham.models.Event`.

    In addition to asking for certain values, the event can also be
    activated.
    """

    def run(self):
        """Run the command."""
        # Get the information.
        name = prompt('Name')
        slug = prompt('Slug (optional)')
        begins = prompt('Event start date')
        ends = prompt('Event end date')
        proposals_begin = prompt('CFP start date')
        active = prompt_bool('Activate the event')

        data = MultiDict({
            'name': name,
            'slug': slug,
            'begins': begins,
            'ends': ends,
            'proposals_begin': proposals_begin,
            'active': active,
        })

        # Validate the form.
        form = EventForm(data, csrf_enabled=False)
        if form.validate():
            # Save the new event.
            event = Event()
            form.populate_obj(event)

            if event.active:
                now = arrow.utcnow().to('America/New_York').naive
                event.activity_begins = now

            db.session.add(event)
            db.session.commit()

            print('\nEvent created successfully.')
            print('Event(id={} slug={} name={})'.format(
                event.id, event.slug, event.name))

            return event

        # If something went wrong, report it and exit out.
        print('\nError creating event:')
        for errors in form.errors.values():
            print('\n'.join(errors))
        sys.exit(1)
