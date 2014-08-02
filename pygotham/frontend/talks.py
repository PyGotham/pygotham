"""PyGotham talks."""

from flask import abort, Blueprint, flash, redirect, render_template, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

from pygotham.core import db
from pygotham.events import get_current as get_current_event
from pygotham.frontend import direct_to_template, route
from pygotham.models import Day, Room, Talk

__all__ = ('blueprint',)

blueprint = Blueprint('talks', __name__, url_prefix='/talks')

direct_to_template(
    blueprint,
    '/call-for-proposals',
    template='talks/call-for-proposals.html',
    endpoint='call_for_proposals',
)


@route(blueprint, '/<int:pk>')
def detail(pk):
    """Return the talk detail view."""
    event = get_current_event()
    if not event.talks_are_published:
        abort(404)

    talk = Talk.query.filter(
        Talk.id == pk,
        Talk.event == event,
        Talk.status == 'accepted').first_or_404()
    return render_template('talks/detail.html', talk=talk)


@route(blueprint, '')
def index():
    """Return the talk list."""
    event = get_current_event()
    if not event.talks_are_published:
        abort(404)

    return render_template('talks/index.html', talks=event.accepted_talks)


@route(
    blueprint,
    '/new',
    defaults={'pk': None},
    endpoint='submit',
    methods=('GET', 'POST'))
@route(blueprint, '/<int:pk>/edit', endpoint='edit', methods=('GET', 'POST',))
@login_required
def proposal(pk=None):
    """Return the talk proposal form."""
    from pygotham.forms import TalkSubmissionForm

    if not (current_user.name and current_user.bio):
        message = 'Please fill out your speaker profile before continuing.'
        flash(message, 'warning')
        return redirect(url_for('profile.settings'))

    event = get_current_event()

    if pk:
        talk = Talk.query.filter(
            Talk.id == pk, Talk.event == event).first_or_404()
        if talk.user != current_user:
            abort(403)
    else:
        if not event.is_call_for_proposals_active:
            # If the current event's CFP is closed, don't allow users to
            # submit new proposals.
            message = 'The Call for Proposals is closed at this time.'
            flash(message, 'warning')
            return redirect(url_for('home.index'))
        talk = Talk(user_id=current_user.id, event=event)
        db.session.add(talk)

    form = TalkSubmissionForm(obj=talk)
    if form.validate_on_submit():
        form.populate_obj(talk)
        db.session.commit()

        flash('Your proposal has been submitted.', 'success')

        return redirect(url_for('profile.dashboard'))

    return render_template('talks/proposal.html', form=form)


@route(blueprint, '/schedule')
def schedule():
    event = get_current_event()
    if not event.talks_are_published:
        abort(404)

    days = Day.query.filter(Day.event == event).order_by(Day.date)

    return render_template('talks/schedule.html', schedule=days)
