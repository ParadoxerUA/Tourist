from helper_classes.base_view import BaseView
from flask import current_app, request, g
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required
from .schemas.role_schema import RoleSchema


class RoleView(BaseView):
    # @login_required
    def post(self):
        try:
            role_data = RoleSchema().load(request.json)
            data = current_app.blueprints['role'].controllers.RoleController.create_role(role_data)
            return self._get_response(data, status_code=201)
        except (ValidationError, Exception) as err:
            data = [str(err)]
            return self._get_response(data, status_code=400)

    # @login_required
    def get(self, trip_id):
        role_data = current_app.blueprints['role'].controllers.RoleController.get_roles(trip_id)
        return self._get_response(role_data, status_code=200)

    def delete(self, trip_id, role_name):
        current_app.blueprints['role'].controllers.RoleController.delete_role(role_name, trip_id)
        return 'Deleted'

