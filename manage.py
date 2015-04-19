"""Management commands."""

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager

from pygotham.factory import create_app
from pygotham.manage import CreateAdmin, CreateUser

manager = Manager(create_app(__name__, ''))
manager.add_command('create_admin', CreateAdmin())
manager.add_command('create_user', CreateUser())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
