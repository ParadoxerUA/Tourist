from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.equipment_schema import EquipmentSchema
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required


class EquipmentView(BaseView):
    def __init__(self):
        self.equipment_controller = current_app.blueprints['equipment'].controllers.EquipmentController

    @login_required
    def get(self, equipment_id):
        response, status_code = self.equipment_controller.get_equipment_data(equipment_id)
        return self._get_response(response, status_code=status_code)

    @login_required
    def put(self, equipment_id):
        try:
            new_equipment_data = EquipmentSchema().load(request.json)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)
        response, status_code = self.equipment_controller.update_equipment(equipment_id, new_equipment_data)
        return self._get_response(response, status_code=status_code)

    @login_required
    def delete(self, equipment_id):
        response, status_code = self.equipment_controller.delete_equipment(equipment_id)
        return self._get_response(response, status_code=status_code)

    @login_required
    def post(self):
        try:
            equipment_data = EquipmentSchema().load(request.json)
        except ValidationError as err:
            return self._get_response(err.messages, status_code=400)
        response, status_code = self.equipment_controller.create_equipment(equipment_data)
        return self._get_response(response, status_code=status_code)
