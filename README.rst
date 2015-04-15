=============
PyGotham 2015
=============

.. image:: https://badge.waffle.io/pygotham/pygotham.png?label=ready&title=Ready
 :target: https://waffle.io/pygotham/pygotham
 :alt: 'Stories in Ready'

Requirements
============

- Python 3.4
- PostgreSQL

Setting up your virtualenv
==========================

We recommend you use pyenv and virtualenvwrapper. Note that in order for pyenv and virtualenvwrapper to play nice
together, you'll want to add the follwing to your ~/.bash_profile::

    export WORKON_HOME="$HOME/.virtualenvs/"

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
        pyenv virtualenvwrapper
    fi

To setup your virtual environment (only need to do once)::

    pyenv local 3.4.3
    mkvirtualenv pygotham

To activate your virtual env (whenever you want to start working the on PyGotham project)::

    workon python

Database Initialization
=======================

Open up PostgreSQL and execute the following::

    create user pygotham with password 'pygotham';
    create database pygotham;
    grant all on database pygotham to pygotham;

Now you'll need to initalize your database. In your terminal shell, run the following commands::

    python manage.py db upgrade
    python manage.py shell

The last command should have opened up a python shell. In the python shell, run the following::

    from pygotham.models import Event
    from datetime import datetime
    from datetime import datetime, timedelta
    from pygotham.core import db
    e = Event(name='PyGotham Test', begins=datetime.now(), ends=(datetime.now() + timedelta(days=365)), active=True)
    db.session.add(e)
    db.session.commit()

Project configuration file
==========================

To create your config settings file, copy the example settings file::

    cp instance/example_settings.cfg instance/settings.cfg


Running the site locally
========================

Now you're ready to start your PyGotham server::

    python wsgi.py

You should see the PyGotham site at::

    http://localhost:5000

