import redis
from flask import current_app, request, g
from .schemas.UserRegisterSchema import UserRegisterSchema
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from apps.user_app.schemas.social_login_schema import SocialLoginSchema
from helper_classes.base_view import BaseView
import facebook
from helper_classes.auth_decorator import login_required


class UserView(BaseView):

    def __init__(self):
        self.user_controller = current_app.blueprints['user'].controllers.UserController

    def post(self):
        # tofix
        request_data = request.json
        try:
            UserRegisterSchema().load(request_data)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=409)

        data = [
            self.user_controller.register_user(**request_data),
        ]
        return self._get_response(data, status_code=201)

    @login_required
    def get(self):
        user_data = self.user_controller.get_user_profile(user_id=g.user_id)

        return self._get_response(data=user_data)

    @login_required
    def patch(self):
        user_data = request.json
        name = user_data['name']
        surname = user_data['surname']
        capacity = user_data['capacity']
        user_profile_controller = current_app.blueprints['user'].controllers.UserController
        user_profile_controller.change_user_data(user_id=g.user_id, capacity=capacity, name=name, surname=surname)
        return self._get_response(f'User`s data updated', status_code=200)


class LoginView(BaseView):
    def __init__(self):
        self.login_controller = current_app.blueprints['user'].controllers.LoginController

    def post(self):
        try:
            user_data = LoginSchema().load(data=request.json)
            session_id = self.login_controller.login(data=user_data)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        return self._get_response(data=session_id)


class SocialLoginView(BaseView):
    def __init__(self):
        self.login_controller = current_app.blueprints['user'].controllers.LoginController

    def post(self):
        try:
            user_data = SocialLoginSchema().load(data=request.json)
            session_id = self.login_controller.login_with_social(data=user_data)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        return self._get_response(data=session_id)


class LogoutView(BaseView):
    @login_required
    def post(self):
        auth_header = request.headers.get('Authorization')
        with redis.Redis() as redis_client:
            redis_client.delete(auth_header)
        return self._get_response(data={'message': 'You successfully logged out.'})