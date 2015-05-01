"""PyGotham user profiles."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

from pygotham.core import db
from pygotham.frontend import route
from pygotham.models import Talk

__all__ = ('blueprint',)

blueprint = Blueprint('profile', __name__, url_prefix='/<event_slug>/profile')


@route(blueprint, '/dashboard')
@login_required
def dashboard():
    """Return the user's dashboard."""
    # TODO: Optionally, old proposals should be shown in a read-only mode.
    talks = Talk.query.current.filter(Talk.user == current_user)
    return render_template(
        'profile/dashboard.html', talks=talks)


@route(blueprint, '/settings', methods=('GET', 'POST'))
@login_required
def settings():
    """Return the user's settings."""
    # TODO: How should this be handled? Should a speaker's bio be stored
    # as a snapshot from event to event? It could be stored as part of a
    # talks.models.Presentation.
    from pygotham.forms import ProfileForm

    form = ProfileForm(request.form, obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()

        flash('Your profile has been updated.', 'success')

        return redirect(url_for('profile.settings'))

    return render_template('profile/settings.html', form=form)
