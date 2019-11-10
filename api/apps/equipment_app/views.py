from helper_classes.base_view import BaseView
from flask import current_app, request
from .schemas.equipment_schema import EquipmentSchema
from marshmallow import ValidationError


class EquipmentView(BaseView):
    def get(self, equipment_id):
        """Return response on get request"""

        try:
            data = current_app.blueprints['equipment'].controllers.EquipmentController.get_equipment_data(equipment_id)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(data, status_code=200)

    def patch(self, equipment_id):
        """Return response on patch request"""

        try:
            new_equipment_data = EquipmentSchema().load(request.json)
            equipment_controller = current_app.blueprints['equipment'].controllers.EquipmentController
            data = equipment_controller.update_equipment(equipment_id, new_equipment_data)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(f"Data successfully updated", status_code=200)

    def delete(self, equipment_id):
        """"Return response on delete request"""

        try:
            data = current_app.blueprints['equipment'].controllers.EquipmentController.delete_equipment(equipment_id)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(f"{data} was successfully deleted", status_code=200)

    def post(self):
        """Return response on post request"""

        try:
            equipment_data = EquipmentSchema().load(request.json)
            data = current_app.blueprints['equipment'].controllers.EquipmentController.create_equipment(equipment_data)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=400)

        return self._get_response(f"{data} was successfully added", status_code=201)
