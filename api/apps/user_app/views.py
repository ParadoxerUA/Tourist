import redis
from flask import current_app, request, g
from .schemas.UserRegisterSchema import UserRegisterSchema
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from apps.user_app.schemas.social_login_schema import SocialLoginSchema
from apps.user_app.schemas.change_password_schema import ChangePasswordSchema
from helper_classes.base_view import BaseView
import facebook
from helper_classes.auth_decorator import login_required
from helper_classes.handy_functions import try_except


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

    # will update user fields
    @login_required
    def put(self):
        return self._get_response('i am UserView.put()')

    # delete user from trip
    @login_required
    def delete(self):
        user_to_delete = request.args.get('user_id')
        trip_id = request.args.get('trip_id')
        if not user_to_delete:
            user_to_delete = g.user_id
        result = self.user_controller.delete_user_from_trip(trip_id, user_to_delete)
        if result:
            return self._get_response(result, status_code=200)
        else:
            return self._get_response('User delete failed', status_code=400)

    @login_required
    def patch(self):
        capacity = request.json
        user_capacity = self.user_controller.change_capacity(user_id=g.user_id, capacity=capacity)
        return self._get_response(f'User new capacity is: {user_capacity}', status_code=200)


class ChangePasswordView(BaseView):
    def __init__(self):
        self.user_controller = current_app.blueprints['user'].controllers.UserController

    @login_required
    def put(self):
        try:
            password_data = ChangePasswordSchema().load(data=request.json)
            data = self.user_controller.change_password(user_id=g.user_id, **password_data)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        return self._get_response(data=data)


class AuthView(BaseView):
    def __init__(self):
        self.login_controller = current_app.blueprints['user'].controllers.LoginController

    # logout
    @login_required
    def get(self):
        with redis.Redis() as redis_client:
            redis_client.delete(g.user_id)
        return self._get_response(data={'message': 'You successfully logged out.'})

    def post(self):
        user_data = try_except(LoginSchema().load, SocialLoginSchema().load, request.json)
        if not user_data:
            return self._get_response('Invalid user data', status_code=400)
        if user_data.get('provider'):
            session_id, user_id = self.login_controller.login_with_social(data=user_data)
        else:
            session_id, user_id = self.login_controller.login(data=user_data)
        return self._get_response({"session_id": session_id, "user_id": user_id}, status_code=201)

class UserTripsView(BaseView):
    # tofix
    def __init__(self):
        self.trip_controller = current_app.blueprints['trip'].controllers.TripController

    @login_required
    def get(self):
        trips_list = self.trip_controller.get_trips_details(g.user_id)
        return self._get_response(trips_list, status_code=200)
