from ..models import Trip
from .point_controller import PointController
from flask import current_app

class TripController:

    @staticmethod
    def _get_session_user_id():
        pass

    @classmethod
    def create_trip(cls, data):
        data['id_admin'] = cls._get_session_user_id()

        trip = current_app.models.Trip.create_trip(data["trip"])
        for point in data["points"]:
            point['id_trip'] = trip.id
            PointController.create_point(point)
        return trip.id
