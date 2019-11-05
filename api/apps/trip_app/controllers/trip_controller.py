from .point_controller import PointController
from flask import current_app
import uuid


class TripController:

    @staticmethod
    def _get_session_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @classmethod
    def create_trip(cls, data, user_id):
        admin = cls._get_session_user(user_id)
        points = []
        for point in data['points']:
            points.append(PointController.create_point(point))
        data['points'] = points
        data['admin'] = admin
        trip = current_app.models.Trip.create_trip(data)
        trip.set_uuid(str(uuid.uuid1()))
        return trip.trip_id

    @classmethod
    def refresh_trip_uuid(cls, trip_id, user_id):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.query.filter_by(trip_id=trip_id).first()
        if trip.admin == user:
            trip.set_uuid(str(uuid.uuid1()))
            return trip.trip_uuid
        else:
            return None

    @classmethod
    def get_trip_data(cls, trip_id, user_id):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.query.filter_by(trip_id=trip_id).first()
        trip_data = trip.get_public_data()
        if trip.admin == user:
            trip_data['trip_uuid'] = trip.trip_uuid
            return trip_data
        else:
            return trip_data

    @classmethod
    def get_user_trips(cls, user_id):
        user = cls._get_session_user(user_id)
        return user.trips

    @classmethod
    def get_trips_details(cls, user_id):
        user = cls._get_session_user(user_id)
        trips_details = [
            trip.get_trip_details() for trip in user.trips
        ]
        return trips_details
