=============
PyGotham 2015
=============

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

- Python 3.4
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

If you choose not to use Docker, you'll need access to Python 3.4 and
PostgreSQL.

The easiest way to manage multiple versions of Python is with pyenv_. A
``.python-version`` file is included in this repository to ensure that the
correct version is always used with the project. Just make sure you install the
appropriate version::

    $ pyenv install 3.4.3

We recommend using a virtual environment to install PyGotham's dependencies. The
easiest way to manage your virtual environments is with virtualenvwrapper_. If
you are using pyenv, you'll want to install pyenv-virtualenvwrapper_.

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

.. note:: If you are using Docker, you'll also need to specify the host
   ``docker-compose run web createdb pygotham -h db``.

Then you'll need to create the tables::

    $ python manage.py db upgrade

The last thing you'll need to do is create a user account. To create a user with
access to the admin::

    $ python manage.py create_admin

Running the site locally
========================

Now you're ready to start your PyGotham server::

    python wsgi.py

You should see the PyGotham site at::

    http://0.0.0.0:5000

If you're using Docker, Compose will take care of running the site for you.


.. _Docker: https://www.docker.com/
.. _Docker Compose: https://docs.docker.com/compose/
.. _PostgreSQL: http://www.postgresql.org/
.. _pyenv: https://github.com/yyuu/pyenv
.. _pyenv-virtualenvwrapper: https://github.com/yyuu/pyenv-virtualenvwrapper
.. _virtualenvwrapper: https://virtualenvwrapper.rtfd.org


.. image:: https://badges.gitter.im/PyGotham/pygotham.svg
   :alt: Join the chat at https://gitter.im/PyGotham/pygotham
   :target: https://gitter.im/PyGotham/pygotham?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge