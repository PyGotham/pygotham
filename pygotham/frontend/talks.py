"""PyGotham talks."""

from flask import Blueprint, render_template
from flask.ext.security import login_required

from pygotham.frontend import route

__all__ = 'blueprint'

blueprint = Blueprint('talks', __name__, url_prefix='/talks')


@route(
    blueprint, '/proposal/new', defaults={'pk': None}, methods=('GET', 'POST'))
@login_required
def proposal(pk):
    """Return the talk proposal form."""
    from pygotham.forms import TalkSubmissionForm

    form = TalkSubmissionForm()

    return render_template('talks/proposal.html', form=form)
