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
    author='Big Apple Py and individual contributors',
    author_email='pygotham@googlegroups.com',
    url='https://github.com/BigApplePy/PyGotham',
    packages=['pygotham'],
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
    install_requires=[
        'Flask==0.10.1',
        'Flask-Admin==1.0.8',
        'Flask-Assets==0.9',
        'Flask-Foundation==2.1',
        'Flask-Login==0.2.11',
        'Flask-Mail==0.9.0',
        'Flask-Migrate==1.2.0',
        'Flask-Principal==0.4.0',
        'Flask-SQLAlchemy==1.0',
        'Flask-Script==2.0.5',
        'Flask-Security==1.7.3',
        'Flask-WTF==0.9.5',
        'Jinja2==2.7.3',
        'Mako==1.0.0',
        'MarkupSafe==0.23',
        'SQLAlchemy==0.9.4',
        'SQLAlchemy-Utils==0.26.2',
        'Unidecode==0.04.16',
        'WTForms==2.0',
        'WTForms-Alchemy==0.12.6',
        'WTForms-Components==0.9.3',
        'Werkzeug==0.9.6',
        'alembic==0.6.5',
        'arrow==0.4.2',
        'bleach==1.4',
        'blinker==1.3',
        'cached-property==0.1.5',
        'cssmin==0.2.0',
        'decorator==3.4.0',
        'docutils==0.11',
        'html5lib==0.999',
        'infinity==1.3',
        'intervals==0.3.0',
        'itsdangerous==0.24',
        'jsmin==2.0.9',
        'passlib==1.6.2',
        'psycopg2==2.5.3',
        'python-dateutil==2.2',
        'python-slugify==0.0.7',
        'six==1.7.2',
        'toolz==0.6.0',
        'validators==0.5.0',
        'webassets==0.9',
    ],
    license=read_file('LICENSE'),
    classifiers=[
    ],
)
