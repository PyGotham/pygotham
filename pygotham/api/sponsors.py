"""Sponsor-related API endpoints."""

from flask import Blueprint
from flask_restful import Api, Resource

from pygotham.events.models import Event
from pygotham.sponsors.models import Level, Sponsor

from .schema import SponsorSchema

blueprint = Blueprint(
    'sponsors',
    __name__,
    subdomain='<event_slug>',
    url_prefix='/events/<int:event_id>/sponsors',
)
api = Api(blueprint)


@api.resource('/')
class SponsorResource(Resource):
    """Represents event sponsors."""

    def get(self, event_id):
        """Return a list of accepted sponsors."""
        event = Event.query.get_or_404(event_id)
        sponsors = Sponsor.query.join(Level).filter(
            Sponsor.accepted == True,  # NOQA
            Level.event == event,
        )
        schema = SponsorSchema(many=True)
        return schema.jsonify(sponsors)
