"""About PyGotham."""

from collections import defaultdict

from flask import Blueprint, render_template, url_for

from pygotham.events import get_current
from pygotham.models import AboutPage

__all__ = ('blueprint', 'get_nav_links')

blueprint = Blueprint('about', __name__, url_prefix='/about')


def get_nav_links():
    """Generates all about page titles and urls for use in the navbar."""
    links = defaultdict(dict)
    for page in AboutPage.query.filter_by(
            active=True, event=get_current()).order_by(AboutPage.slug):
        url = url_for('about.rst_content', slug=page.slug)
        links[page.navbar_section.lower()][page.title] = url
    return links


@blueprint.route('/<slug>')
def rst_content(slug):
    """Renders database-backed restructured text content as html pages.

    :param slug: the uniquely identifying slug portion of the url
    """
    page = AboutPage.query.filter_by(
        slug=slug,
        active=True,
        event=get_current(),
    ).first_or_404()
    return render_template('about/rst.html', page=page)
