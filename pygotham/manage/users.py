"""User-related management commands."""

import sys

from flask import current_app
from flask_script import Command, prompt, prompt_pass
from flask_security.forms import RegisterForm
from flask_security.registerable import register_user
from werkzeug.datastructures import MultiDict


class RegisterUserMixin:

    """Mixin that provides functionality to register new users."""

    def register_user(self):
        """Prompt for user details."""
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

            return user

        # If something went wrong, report it and exit out.
        print('\nError creating user:')
        for errors in form.errors.values():
            print('\n'.join(errors))
        sys.exit(1)


class CreateAdmin(Command, RegisterUserMixin):

    """Management command to create a :class:`~pygotham.models.User`.

    Users created through this command will have the ``admin`` role
    associated with them.
    """

    def run(self):
        """Run the command."""
        user = self.register_user()

        if user:
            # Add the new user to the admin role.
            datastore = current_app.extensions['security'].datastore
            role = datastore.find_or_create_role(
                'admin', description='Administrator')
            datastore.add_role_to_user(user, role)

            datastore.commit()

            print('\nUser added to admins.')

            return

        # If something went wrong, report it and exit out.
        print('\nError add user to admins')
        sys.exit(1)


class CreateUser(Command, RegisterUserMixin):

    """Management command to create a :class:`~pygotham.models.User`."""

    def run(self):
        """Run the command."""
        self.register_user()
