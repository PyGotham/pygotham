"""Event-related API endpoints."""

from flask import Blueprint
from flask_restful import Api, Resource

from pygotham.events.models import Event

from .schema import EventSchema


blueprint = Blueprint(
    'events', __name__, subdomain='<event_slug>', url_prefix='/events')
api = Api(blueprint)


@api.resource('/')
class EventListResource(Resource):
    """Return all available event data."""

    def get(self):
        """Event list."""
        schema = EventSchema(many=True)
        return schema.jsonify(Event.query.filter_by(active=True).all())


@api.resource('/<int:event_id>/')
class EventResource(Resource):
    """Return event core data."""

    def get(self, event_id):
        """Event details."""
        schema = EventSchema()
        return schema.jsonify(
            Event.query.filter_by(active=True, id=event_id).first_or_404())
