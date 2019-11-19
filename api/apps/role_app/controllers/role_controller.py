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

    @staticmethod
    def _get_role(role_id):
        role = current_app.models.Role.get_role_by_id(role_id)
        return role

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

    @classmethod
    def toggle_role(cls, role_id, user_id, admin_id):
        role = cls._get_role(role_id)
        user = cls._get_user(user_id)
        admin = cls._get_user(admin_id)
        trip = cls._get_trip(role.trip_id)
        if trip.admin == admin and user in trip.users:
            return role.toggle_role(user)
        else:
            return None

    @staticmethod
    def delete_role(role_name, trip_id):
        current_app.models.Role.delete_role(role_name, trip_id)
