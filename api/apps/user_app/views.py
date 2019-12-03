import redis
from flask import current_app, request, g
from .schemas.UserRegisterSchema import UserRegisterSchema
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from apps.user_app.schemas.social_login_schema import SocialLoginSchema
from apps.user_app.schemas.update_user_schema import UpdateUserSchema
from helper_classes.base_view import BaseView
import facebook
from helper_classes.auth_decorator import login_required
from helper_classes.handy_functions import try_except


class UserView(BaseView):

    def __init__(self):
        self.user_controller = current_app.blueprints['user'].controllers.UserController

    def post(self):
        # tofix
        try:
            request_data = UserRegisterSchema().load(request.json)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=409)
        response, status_code = self.user_controller.register_user(**request_data)
        return self._get_response(response, status_code=status_code)

    @login_required
    def get(self):
        fields = request.args.get('fields')
        trip_id = request.args.get('trip_id')
        if fields:
            fields = fields.split(',')&trip_id=
        response, status_code = self.uer_controller.get_user_data(fields, trip_id=trip_id)
        return self._get_response(response, status_code=status_code)

    # will update user fields
    @login_required
    def put(self):
        return self._get_response('i am UserView.put()')

    # delete user from trip
    @login_required
    def delete(self):
        user_to_delete = request.args.get('user_id') or g.user_id
        trip_id = request.args.get('trip_id')
        result, status_code = self.user_controller.delete_user_from_trip(trip_id, user_to_delete)
        return self._get_response(result, status_code=status_code)

    @login_required
    def patch(self):
        try:
            data = UpdateUserSchema().load(data=request.json)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        if data.get('new_password'):
            message, status_code = self.user_controller.change_password(**data)
        else:
            message, status_code = self.user_controller.update_user(data)
        return self._get_response(data=message, status_code=status_code)


class LoginView(BaseView):
    def __init__(self):
        self.login_controller = current_app.blueprints['user'].controllers.LoginController

    def post(self):
        user_data = try_except(LoginSchema().load, SocialLoginSchema().load, request.json)
        if not user_data:
            return self._get_response('Invalid user data', status_code=400)
        if user_data.get('provider'):
            session_id, user_id = self.login_controller.login_with_social(data=user_data)
        else:
            session_id, user_id = self.login_controller.login(data=user_data)
        return self._get_response({"session_id": session_id, "user_id": user_id}, status_code=201)

class LogoutView(BaseView):
    @login_required
    def post(self):
        with redis.Redis() as redis_client:
            redis_client.delete(g.user_id)
            redis_client.delete(request.headers.get('Authorization'))
        return self._get_response('You successfully logged out.')

