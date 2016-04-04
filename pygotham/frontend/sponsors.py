"""PyGotham sponsor profiles."""

from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for,
)
from flask_login import current_user
from flask_security import login_required
from sqlalchemy import inspect

from pygotham.core import db
from pygotham.frontend import direct_to_template, route
from pygotham.models import Level, Sponsor

__all__ = ('blueprint',)

blueprint = Blueprint(
    'sponsors',
    __name__,
    subdomain='<event_slug>',
    url_prefix='/sponsors',
)


@route(blueprint, '/apply/', methods=('GET', 'POST'))
@login_required
def apply():
    """Return the sponsor application."""
    from pygotham.forms import SponsorApplicationForm

    form = SponsorApplicationForm(
        request.form,
        applicant_id=current_user.id,
        contact_name=current_user.name,
        contact_email=current_user.email)

    if form.validate_on_submit():
        sponsor = Sponsor()
        form.populate_obj(sponsor)
        sponsor.applicant_id = current_user.id

        # form.populate_obj already associated the instance with a
        # session.
        session = inspect(sponsor).session
        session.commit()

        flash('Your application has been submitted.', 'success')

        return redirect(url_for('sponsors.apply'))

    return render_template('sponsors/apply.html', form=form)


@route(blueprint, '/edit/<int:pk>/', methods=('GET', 'POST'))
@login_required
def edit(pk):
    """Return the sponsor edit form."""
    sponsor = Sponsor.query.get_or_404(pk)
    if sponsor.applicant != current_user:
        abort(403)

    # TODO: Restrict by event.

    from pygotham.forms import SponsorEditForm

    form = SponsorEditForm(obj=sponsor)
    if form.validate_on_submit():
        form.populate_obj(sponsor)
        db.session.commit()

        flash('Your application has been updated.', 'success')

        return redirect(url_for('profile.dashboard'))

    return render_template('sponsors/edit.html', form=form, sponsor=sponsor)


@route(blueprint, '/', navbar_kwargs={'path': ('Sponsors', 'Sponsors')})
def index():
    """Return the sponsors."""
    levels = Level.query.current.order_by(Level.order)
    sponsors = Sponsor.query.join(Level).filter(
        Sponsor.accepted == True,  # NOQA
        Level.event == g.current_event,
    )
    has_sponsors = db.session.query(sponsors.exists()).scalar()
    return render_template(
        'sponsors/index.html', levels=levels, has_sponsors=has_sponsors)


@route(
    blueprint,
    '/prospectus/',
    navbar_kwargs={'path': ('Sponsors', 'Sponsorship Prospectus')})
def prospectus():
    """Return the sponsorship prospectus."""
    levels = Level.query.current.order_by(Level.order)
    return render_template('sponsors/prospectus.html', levels=levels)


# TODO: Add this to the navbar.
# FIXME: This content seems to be missing. Probably a template issue.
# This is a good candidate for switching to an AboutPage.
direct_to_template(blueprint, '/terms/', template='sponsors/terms.html')
