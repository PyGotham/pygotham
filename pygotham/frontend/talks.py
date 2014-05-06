"""PyGotham talks."""

from flask import abort, Blueprint, flash, redirect, render_template, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

from pygotham.core import db
from pygotham.events import get_current
from pygotham.frontend import route
from pygotham.models import Talk

__all__ = 'blueprint'

blueprint = Blueprint('talks', __name__, url_prefix='/talks')


@route(
    blueprint, '/new', defaults={'pk': None}, endpoint='submit', methods=('GET', 'POST'))
@route(blueprint, '/<int:pk>/edit', endpoint='edit', methods=('GET', 'POST',))
@login_required
def proposal(pk=None):
    """Return the talk proposal form."""
    from pygotham.forms import TalkSubmissionForm

    event = get_current()

    if pk:
        talk = Talk.query.filter(
            Talk.id == pk, Talk.event == event).first_or_404()
        if talk.user != current_user:
            abort(403)
    else:
        talk = Talk(user_id=current_user.id, event=event)
        db.session.add(talk)

    form = TalkSubmissionForm(obj=talk)
    if form.validate_on_submit():
        form.populate_obj(talk)
        db.session.commit()

        flash('You proposal has been submitted.', 'success')

        return redirect(url_for('profile.index'))

    return render_template('talks/proposal.html', form=form)
