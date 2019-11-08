from .point_controller import PointController
from flask import current_app, g
import uuid


class TripController:

    @staticmethod
    def _get_session_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @classmethod
    def create_trip(cls, data, user_id):
        admin = cls._get_session_user(user_id)
        data['admin'] = admin
        points = data.pop('points', None)
        trip = current_app.models.Trip.create_trip(data)
        for point in points:
            PointController.create_point(point, trip)
        trip.set_uuid(str(uuid.uuid1()))
        return trip.trip_id

    @classmethod
    def refresh_trip_uuid(cls, trip_id, user_id):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        if trip.admin == user:
            trip.set_uuid(str(uuid.uuid1()))
            return trip.trip_uuid
        else:
            return None

    @classmethod
    def get_trip_data(cls, trip_id, user_id, fields):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.get_trip_by_id(trip_id=trip_id)
        trip_data = trip.get_fields(fields)
        if trip_data.get('trip_uuid') and trip.admin != user:
            del trip_data['trip_uuid']
        return trip_data

    @classmethod
    def get_user_trips(cls, user_id):
        user = cls._get_session_user(user_id)
        return user.trips

    @classmethod
    def get_trips_details(cls, user_id):
        user = cls._get_session_user(user_id)
        trips_details = [
            trip.get_trip_details(user_id) for trip in user.trips
        ]
        return trips_details

    @classmethod
    def user_to_trip(cls, trip_uuid, user_id):
        user = cls._get_session_user(user_id)
        trip = current_app.models.Trip.get_trip_by_uuid(trip_uuid=trip_uuid)
        try:
            trip.join_user(user)
            return 'User assigned to trip'
        except:
            return None

    @classmethod
    def delete_user_from_trip(cls, trip_id, user_to_delete):
        trip = current_app.models.Trip.get_trip_by_id(trip_id=trip_id)
        if (user_to_delete != g.user_id) and (g.user_id != trip.admin_id):
            return None
        user = cls._get_session_user(user_to_delete)
        return trip.delete_user(user)

