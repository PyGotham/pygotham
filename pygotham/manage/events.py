"""Event-related management commands."""

import os
import sys

import arrow
from flask import current_app
from flask_script import Command, prompt, prompt_bool
from slugify import slugify
from werkzeug.datastructures import MultiDict

from pygotham.core import db
from pygotham.forms import EventForm
from pygotham.models import AboutPage, Event

PAGES = {'Code of Conduct', 'Privacy Policy'}
TEMPLATE_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'templates')


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

        add_pages = prompt_bool('Add About pages')

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
                now = arrow.utcnow().to(current_app.config['TIME_ZONE']).naive
                event.activity_begins = now

            db.session.add(event)

            if add_pages:
                for title in PAGES:
                    # While the slug will be automatically generated
                    # when an instance of AboutPage is saved, it's
                    # needed to open the correct file.
                    slug = slugify(title)

                    file = os.path.join(TEMPLATE_PATH, slug + '.rst')
                    with open(file) as f:
                        AboutPage(
                            title=title,
                            slug=slug,
                            content=f.read(),
                            navbar_path=['About', title],
                            event=event,
                            active=True,
                        )

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
