from .point_controller import PointController
from flask import current_app
import redis, json, uuid


class TripController:

    @staticmethod
    def _get_session_user(session_id):
        with redis.Redis() as redis_client:
            session_data = json.loads(redis_client.get(session_id))
        user = current_app.models.User.get_user_by_id(session_data['user_id'])
        return user

    @classmethod
    def create_trip(cls, data, session_id):
        admin = cls._get_session_user(session_id)
        points = []
        for point in data['points']:
            points.append(PointController.create_point(point))
        data['points'] = points
        data['admin'] = admin
        trip = current_app.models.Trip.create_trip(data)
        trip.set_uuid(str(uuid.uuid1()))
        return trip.trip_id

    @classmethod
    def refresh_trip(cls, trip_id, session_id):
        user = cls._get_session_user(session_id)
        trip = current_app.models.Trip.query.filter_by(trip_id=trip_id).first()
        if trip.admin == user:
            trip.set_uuid(str(uuid.uuid1()))
            return trip.trip_uuid
        else:
            return None

    @classmethod
    def get_trip_uuid(cls, trip_id, session_id):
        user = cls._get_session_user(session_id)
        trip = current_app.models.Trip.query.filter_by(trip_id=trip_id).first()
        if trip.admin == user:
            return trip.trip_uuid
        else:
            return None

