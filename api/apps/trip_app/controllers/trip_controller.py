from apps.trip_app.models import Trip

class TripController:

    @staticmethod
    def _get_session_user_id():
        pass

    @classmethod
    def add_trip(cls, data):
        data['id_admin'] = cls._get_session_user_id()
        return Trip.create_trip(data)
