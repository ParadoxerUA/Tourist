from flask import current_app


class RoleController:

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @classmethod
    def create_role(cls, data, user_id):
        user = cls._get_user(user_id)
        trip = cls._get_trip(data['trip_id'])
        if user == trip.admin:
            role = current_app.models.Role.create_role(data)
        else:
            role = None
        return role

    @classmethod
    def get_roles(cls, trip_id):
        trip = cls._get_trip(trip_id)
        return trip.roles

    @staticmethod
    def delete_role(role_name, trip_id):
        current_app.models.Role.delete_role(role_name, trip_id)
