"""PyGotham talks."""

from flask import (abort, Blueprint, g, flash, redirect, render_template,
                   url_for)
from flask_login import current_user
from flask_security import login_required

from pygotham.core import db
from pygotham.frontend import direct_to_template, route
from pygotham.models import Day, Talk

__all__ = ('blueprint',)

blueprint = Blueprint(
    'talks',
    __name__,
    subdomain='<event_slug>',
    url_prefix='/talks',
)

direct_to_template(
    blueprint,
    '/call-for-proposals/',
    template='talks/call-for-proposals.html',
    endpoint='call_for_proposals',
    navbar_kwargs={'path': ('Speaking', 'Call for Proposals')},
)


# This route is being kept around for backward compatibility. It should
# never be used directly.
@route(
    blueprint, '/<int:pk>/', defaults={'slug': None}, endpoint='old_detail')
@route(blueprint, '/<int:pk>/<slug>/')
def detail(pk, slug):
    """Return the talk detail view."""
    event = g.current_event
    if not event.talks_are_published:
        abort(404)

    talk = Talk.query.filter(
        Talk.id == pk,
        Talk.event == event,
        Talk.status == 'accepted').first_or_404()

    if slug != talk.slug:
        return redirect(url_for('talks.detail', pk=pk, slug=talk.slug))

    return render_template('talks/detail.html', talk=talk)


@route(
    blueprint,
    '/',
    navbar_kwargs={
        'path': ('Events', 'Talk List'),
        'when': lambda: g.current_event.talks_are_published,
    })
def index():
    """Return the talk list."""
    event = g.current_event
    if not event.talks_are_published:
        abort(404)

    return render_template('talks/index.html', talks=event.accepted_talks)


@route(
    blueprint,
    '/new/',
    defaults={'pk': None},
    endpoint='submit',
    methods=('GET', 'POST'),
    navbar_kwargs={
        'path': ('Speaking', 'Submit a Talk'),
        'when': lambda: g.current_event.is_call_for_proposals_active,
    })
@route(blueprint, '/<int:pk>/edit/', endpoint='edit', methods=('GET', 'POST',))
@login_required
def proposal(pk=None):
    """Return the talk proposal form."""
    from pygotham.forms import TalkSubmissionForm

    if not (current_user.name and current_user.bio):
        message = 'Please fill out your speaker profile before continuing.'
        flash(message, 'warning')
        return redirect(url_for('profile.settings'))

    event = g.current_event

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
        talk = Talk(
            user_id=current_user.id,
            event_id=event.id,
            recording_release=True,
            type='talk',
        )

    form = TalkSubmissionForm(obj=talk)
    if form.validate_on_submit():
        form.populate_obj(talk)

        db.session.add(talk)
        db.session.commit()

        flash('Your proposal has been submitted.', 'success')

        return redirect(url_for('profile.dashboard'))

    return render_template('talks/proposal.html', form=form)


direct_to_template(
    blueprint,
    '/recording/',
    template='talks/recording-release.html',
    endpoint='recording_release',
)


@route(
    blueprint,
    '/schedule/',
    navbar_kwargs={
        'path': ('Events', 'Talk Schedule'),
        'when': lambda: g.current_event.schedule_is_published,
    })
def schedule():
    event = g.current_event
    if not (event.schedule_is_published or current_user.has_role('admin')):
        abort(404)

    days = Day.query.filter(Day.event == event).order_by(Day.date)

    return render_template('talks/schedule.html', schedule=days)
