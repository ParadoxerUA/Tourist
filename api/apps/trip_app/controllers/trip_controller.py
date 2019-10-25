from ..models import Trip
from apps.user_app.models import User
from .point_controller import PointController
from flask import current_app
import redis, json


class TripController:

    @staticmethod
    def _get_session_user(session_id):
        with redis.Redis() as redis_client:
            session_data = json.loads(redis_client.get(session_id))
        user = User.get_user(user_id=session_data['user_id'])
        return user

    @classmethod
    def create_trip(cls, data, session_id):
        admin = cls._get_session_user(session_id)
        points = []
        for point in data['points']:
            points.append(PointController.create_point(point))
        data['points'] = points
        data['admin'] = admin
        trip = Trip.create_trip(data)
        return trip.trip_id
