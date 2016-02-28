"""About PyGotham."""

from flask import Blueprint, render_template

from pygotham.models import AboutPage

__all__ = ('blueprint',)

blueprint = Blueprint('about', __name__, url_prefix='/<event_slug>/about')


@blueprint.route('/<slug>/')
def rst_content(slug):
    """Renders database-backed restructured text content as html pages.

    :param slug: the uniquely identifying slug portion of the url
    """
    page = AboutPage.query.current.filter_by(
        slug=slug,
        active=True,
    ).first_or_404()
    return render_template('about/rst.html', page=page)
