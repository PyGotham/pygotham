"""Schedule-related API endpoints."""

from flask import Blueprint
from flask_restful import Api, Resource

from pygotham.events.models import Event
from pygotham.talks.models import Talk

from .schema import TalkSchema

blueprint = Blueprint(
    'schedule',
    __name__,
    subdomain='<event_slug>',
    url_prefix='/events/<int:event_id>/schedule',
)
api = Api(blueprint)


@api.resource('/')
class TalkResource(Resource):
    """Represents talks and their place on the schedule."""

    def get(self, event_id):
        """Return a list of accepted talks."""
        event = Event.query.get_or_404(event_id)
        talks = Talk.query.filter_by(event=event, status='accepted').all()
        schema = TalkSchema(many=True)
        return schema.jsonify(talks)
