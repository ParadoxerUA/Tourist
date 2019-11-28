from helper_classes.base_view import BaseView
from flask import current_app, request, g
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required
from .schemas.role_schema import RoleSchema


class RoleView(BaseView):
    def __init__(self):
        self.role_controller = current_app.blueprints['role'].controllers.RoleController


    @login_required
    def post(self):
        try:
            role_data = RoleSchema().load(request.json)
        except (ValidationError, Exception) as err:
            return self._get_response(str(err), status_code=400)
        data = self.role_controller.create_role(role_data, g.user_id)
        print('print from RoleView.post')
        print(data)
        if data:
            return self._get_response(data, status_code=201)
        else:
            return self._get_response('Creating role failed', status_code=400)

    @login_required
    def get(self, role_id):
        role_data = self.role_controller.get_role(role_id)
        return self._get_response(role_data, status_code=200)

    @login_required
    def delete(self, role_id):
        self.role_controller.delete_role(role_id)
        return 'Deleted'

    @login_required
    def put(self, role_id):
        user_id = request.json.get('user_id')
        result = self.role_controller.toggle_role(role_id, user_id, g.user_id)
        if result:
            return self._get_response(result, status_code=201)
        else:
            return self._get_response('Assigning role failed', status_code=400)


