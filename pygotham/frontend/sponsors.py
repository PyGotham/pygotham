"""PyGotham sponsor profiles."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import current_user
from flask.ext.security import login_required

from pygotham.core import db
from pygotham.frontend import direct_to_template, route
from pygotham.models import Sponsor

__all__ = 'blueprint',

blueprint = Blueprint('sponsors', __name__, url_prefix='/sponsors')


@route(blueprint, '/apply', methods=('GET', 'POST'))
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

        db.session.commit()

        flash('Your application has been submitted.', 'success')

        return redirect(url_for('sponsors.apply'))

    return render_template('sponsors/apply.html', form=form)


@route(blueprint, '')
def index():
    """Return the sponsors."""
    return render_template('sponsors/index.html')


direct_to_template(
    blueprint, 'prospectus', template='sponsors/prospectus.html')


direct_to_template(blueprint, '/terms', template='sponsors/terms.html')
