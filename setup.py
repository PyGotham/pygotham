from setuptools import setup


def read_file(filename):
    try:
        with open(filename) as f:
            return f.read()
    except IOError:
        return ''


setup(
    name='PyGotham',
    version='2014.1',
    description='Site for PyGotham 2014',
    long_description=read_file('README.rst'),
    author='Andy Dirnberger',
    author_email='dirn@dirnonline.com',
    url='https://github.com/BigApplePy/PyGotham',
    packages=['pygotham'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    install_requires=[
        'Flask==0.10.1',
        'Flask-Admin==1.0.7',
        'Flask-Assets==0.9',
        'Flask-Foundation==2.1',
        'Flask-Login==0.2.9',
        'Flask-Mail==0.9.0',
        'Flask-Migrate==1.2.0',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==1.0',
        'Flask-Script==0.6.7',
        'Flask-Security==1.7.1',
        'Flask-WTF==0.9.4',
        'Jinja2==2.7.2',
        'Mako==0.9.1',
        'MarkupSafe==0.18',
        'SQLAlchemy==0.9.3',
        'SQLAlchemy-Utils==0.24.1',
        'WTForms==1.0.5',
        'WTForms-Alchemy==0.12.2',
        'WTForms-Components==0.9.1',
        'Werkzeug==0.9.4',
        'alembic==0.6.3',
        'blinker==1.3',
        'decorator==3.4.0',
        'infinity==1.3',
        'intervals==0.2.3',
        'itsdangerous==0.23',
        'passlib==1.6.2',
        'psycopg2==2.5.2',
        'six==1.5.2',
        'toolz==0.5.2',
        'validators==0.5.0',
        'webassets==0.9',
    ],
    license=read_file('LICENSE'),
    classifiers=[
    ],
)
