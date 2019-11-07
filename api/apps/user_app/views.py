import redis
from flask import current_app, request, g
from .schemas.UserRegisterSchema import UserRegisterSchema
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from apps.user_app.schemas.social_login_schema import SocialLoginSchema
from helper_classes.base_view import BaseView
import facebook
from helper_classes.auth_decorator import login_required


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

<<<<<<< HEAD
class SocialLoginView(BaseView):
    def post(self):
        try:
            user_data = SocialLoginSchema().load(data=request.json)
            data = current_app.blueprints['user'].controllers.LoginController.login_with_social(user_data)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        return self._get_response(data)
=======

class LogoutView(BaseView):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return self._get_response(data={'message': 'No authorization header provided.'}, status_code=403)

        with redis.Redis() as redis_client:
            redis_client.delete(auth_header)

        return self._get_response(data={'message': 'You successfully logged out.'})


class UserProfileView(BaseView):
    @login_required
    def get(self):
        user_profile_controller = current_app.blueprints['user'].controllers.UserProfileController
        user_profile_data = user_profile_controller.get_user_profile(user_id=g.user_id)

        return self._get_response(data=user_profile_data)
>>>>>>> development
