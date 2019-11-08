from flask import current_app


class RoleController:

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @staticmethod
    def create_role(data):
        role = current_app.models.Role.create_role(data)
        return role

    @classmethod
    def get_roles(cls, trip_id):
        trip = cls._get_trip(trip_id)
        return trip.roles

    @staticmethod
    def delete_role(role_name, trip_id):
        current_app.models.Role.delete_role(role_name, trip_id)
