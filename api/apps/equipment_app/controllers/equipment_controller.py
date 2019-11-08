from apps.equipment_app.models import Equipment


class EquipmentController:

    @classmethod
    def get_equipment_data(cls, equipment_id):
        equipment_data = Equipment.get_equipment_by_id(equipment_id)
        return equipment_data

    @classmethod
    def update_equipment(cls, equipment_id, data):
        new_equipment = Equipment.update_equipment(equipment_id, data)
        return new_equipment

    @classmethod
    def delete_equipment(cls, equipment_id):
        equipment_data = Equipment.delete_equipment(equipment_id)
        return equipment_data

    @classmethod
    def create_equipment(cls, data):
        data = Equipment.create_equipment(data)
        return data
