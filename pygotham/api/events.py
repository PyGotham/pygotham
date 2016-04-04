"""Event-related API endpoints."""

from flask import Blueprint
from flask_restful import Api, Resource, marshal_with

from pygotham.events.models import Event

from .fields import event_fields


blueprint = Blueprint('events', __name__, url_prefix='/events')
api = Api(blueprint)


@api.resource('/')
class EventListResource(Resource):
    """Return all available event data."""

    @marshal_with(event_fields)
    def get(self):
        """Event list."""
        return Event.query.filter_by(active=True).all()


@api.resource('/<int:event_id>/')
class EventResource(Resource):
    """Return event core data."""

    @marshal_with(event_fields)
    def get(self, event_id):
        """Event details."""
        return Event.query.filter_by(active=True, id=event_id).first_or_404()
