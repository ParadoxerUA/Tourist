from flask import g, current_app


class EquipmentController:
    @classmethod
    def _user_has_privileges(cls, trip_id=None, role_id=None, owner_id=None):
        user = cls._get_user(g.user_id)
        trip = cls._get_trip(trip_id)
        user_has_role = role_id in (role.id for role in user.roles)
        is_item_owner = owner_id == user.user_id
        is_admin = user == trip.admin
        return user_has_role or is_item_owner or is_admin

    @staticmethod
    def _get_eq(equipment_id):
        eq = current_app.models.Equipment.get_equipment_by_id(equipment_id)
        return eq

    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @classmethod
    def get_equipment_data(cls, equipment_id):
        equipment = cls._get_eq(equipment_id)
        user = cls._get_user(g.user_id)
        if equipment.trip in user.trips:
            return equipment, 201
        return 'You are not member of current trip', 402

    @classmethod
    def update_equipment(cls, equipment_id, data):
        item = cls._get_eq(equipment_id)
        if cls._user_has_privileges(item.trip_id, item.role_id, item.owner_id):
            response = current_app.models.Equipment.update_equipment(equipment_id, data)
            return response, 201
        return 'You dont have rights', 402

    @classmethod
    def delete_equipment(cls, equipment_id):
        item = cls._get_eq(equipment_id)
        if cls._user_has_privileges(item.trip_id, item.role_id, item.owner_id):
            response = current_app.models.Equipment.delete_equipment(equipment_id)
            return response, 201
        return 'You dont have rights', 402

    @classmethod
    def create_equipment(cls, data):
        if cls._user_has_privileges(data['trip_id'], data.get('role_id'), data.get('owner_id')):
            response = current_app.models.Equipment.create_equipment(data)
            return response, 201
        return 'You dont have rights', 402
