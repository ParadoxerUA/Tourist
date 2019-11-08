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
    def get_trip_data(cls, trip_id, user_id, fields):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.query.filter_by(trip_id=trip_id).first()
        trip_data = trip.get_fields(*fields)
        if trip.admin == user:
            return trip_data
        else:
            try:
                del trip_data['trip_uuid']
            except KeyError:
                pass
            return trip_data

    @classmethod
    def get_user_trips(cls, user_id):
        user = cls._get_session_user(user_id)
        return user.trips

    @classmethod
    def user_to_trip(cls, trip_uuid, user_id):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.query.filter_by(trip_uuid=trip_uuid).first()
        try:
            trip.join_user(user)
            return f'{user.email} assign to trip.trip_id={trip.trip_id}'
        except:
            return None
