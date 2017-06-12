========
PyGotham
========

.. note::

    This repository is no longer maintained. The next iteration of the website
    can be found at https://gitlab.com/pygotham/2017. Thanks to everyone who
    contributed!

.. image:: https://badge.waffle.io/pygotham/pygotham.png?label=ready&title=Ready
   :target: https://waffle.io/pygotham/pygotham
   :alt: 'Stories in Ready'

.. image:: https://requires.io/github/PyGotham/pygotham/requirements.svg?branch=master
   :target: https://requires.io/github/PyGotham/pygotham/requirements/?branch=master
   :alt: Requirements Status

Requirements
============

- Docker_

or

- Python 3.5
- PostgreSQL_

Getting started
===============

The simplest way to create an environment for working on PyGotham is to use
Docker and `Docker Compose`_. Installing Docker is beyond the scope of these
instructions, but once you have each tool installed, a new environment can be
created by executing the following commands from within the folder where you've
closed this repository::

    $ docker-compose build
    $ docker-compose up -d

Alternate setup
---------------

If you choose not to use Docker, you'll need access to Python 3.5 and
PostgreSQL.

The easiest way to manage multiple versions of Python is with pyenv_. A
``.python-version`` file is included in this repository to ensure that the
correct version is always used with the project. Just make sure you install the
appropriate version::

    $ pyenv install 3.5.1

We recommend using a virtual environment to install PyGotham's dependencies. The
easiest way to manage your virtual environments is with virtualenvwrapper_. If
you are using pyenv, you'll want to install pyenv-virtualenvwrapper_.

You'll also need to install the project's requirements::

    $ python -m pip install -r dev-requirements.txt

Project configuration
=====================

An example configuration file is included in the repository. It can be used as
the basis for your local settings::

    $ cp instance/example_settings.cfg instance/settings.cfg

If you are using Docker, this file can be used as-is. If you aren't, make sure
you update ``SQLALCHEMY_DATABASE_URI`` to include the correct URI for your
database.

Database initialization
=======================

If you are using Docker, make sure to run the commands in this section through
``docker-compose run web``.

When you first get started, you'll need to create the database::

    $ createdb pygotham

.. note:: If you are using Docker, Compose will take care of for you.

Then you'll need to create the tables::

    $ python manage.py db upgrade

Next, you'll need to create a user account. To create a user with
access to the admin::

    $ python manage.py create_admin
    Email: <email>
    Name: <name>
    Password: <password>
    Confirm Password: <password>

The last step is to create an event::

    $ python manage.py create_event
    Name: <name>
    Slug (optional): <slug>
    Event start date: <YYYY-MM-DD>
    Event end date: <YYYY-MM-DD>
    CFP start date: <YYYY-MM-DD HH:MM:SS>
    Activate the event [n]: <y|n>


Running the site locally
========================
The ``SERVER_NAME`` environment variable must be set to develop locally.
Because of how web browsers treat cookies on domains, this value must have a
``.`` in it. Before launching a development server::

    $ export SERVER_NAME=pygotham.local:5000

Now you're ready to start your PyGotham server::

    $ python wsgi.py

You should see the PyGotham site at::

    http://<slug>.$SERVER_NAME

where ``<slug>`` is the slug of the event created by the ``create_event``
management command.

.. note:: If you're using Docker, Compose will take care of running the site
   for you.

Adding requirements
===================

New requirements should be added to ``requirements.in``. An updated
``requirements.txt`` can be generated using::

    $ pip-compile requirements.in

.. _Docker: https://www.docker.com/
.. _Docker Compose: https://docs.docker.com/compose/
.. _PostgreSQL: http://www.postgresql.org/
.. _pyenv: https://github.com/yyuu/pyenv
.. _pyenv-virtualenvwrapper: https://github.com/yyuu/pyenv-virtualenvwrapper
.. _virtualenvwrapper: https://virtualenvwrapper.rtfd.org
