"""User-related management commands."""

import sys

from flask.ext.script import Command, prompt, prompt_pass
from flask.ext.security.forms import RegisterForm
from flask.ext.security.registerable import register_user
from werkzeug.datastructures import MultiDict


class CreateUser(Command):

    """Management command to create a :class:`~pygotham.models.User`."""

    def run(self):
        """Run the command."""
        # Get the information.
        email = prompt('Email')
        name = prompt('Name')
        password = prompt_pass('Password')
        password_confirm = prompt_pass('Confirm Password')
        data = MultiDict({
            'email': email,
            'password': password,
            'password_confirm': password_confirm,
        })

        # Validate the form.
        form = RegisterForm(data, csrf_enabled=False)
        if form.validate():
            # Register the new user.
            user = register_user(name=name, email=email, password=password)
            print('\nUser created successfully.')
            print('User(id={} email={})'.format(user.id, user.email))

            return

        # If something went wrong, report it and exit out.
        print('\nError creating user:')
        for errors in form.errors.values():
            print('\n'.join(errors))
        sys.exit(1)
