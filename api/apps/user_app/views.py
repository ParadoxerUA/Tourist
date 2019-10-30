import redis
from flask import current_app, request
from .schemas.UserRegisterSchema import UserRegisterSchema
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from helper_classes.base_view import BaseView


class UserRegistrationView(BaseView):
    def post(self):

        request_data = request.json
        try:
            UserRegisterSchema().load(request_data)
        except ValidationError as err:
            return self._get_response(data=err.messages, status_code=409)

        data = [
            current_app.blueprints['user'].controllers.UserController.register_user(**request_data),
        ]
        return self._get_response(data, status_code=201)


class LoginView(BaseView):
    def post(self):
        try:
            user_data = LoginSchema().load(data=request.json)
            session_id = current_app.blueprints['user'].controllers.LoginController.login(data=user_data)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)

        response = self._get_response(data=session_id)
        response.headers['Authorization'] = session_id
        return response


class LogoutView(BaseView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return self._get_response(data={'message': 'No authorization header provided.'}, status_code=403)
        with redis.Redis() as redis_client:
            redis_client.delete(auth_header)
            return self._get_response(data={'message': 'You successfully logged out.'}, status_code=200)
