from flask import current_app, request
from marshmallow import ValidationError
from apps.user_app.schemas.login_schema import LoginSchema
from helper_classes.base_view import BaseView


class UserRegistrationView(BaseView):
    def post(self):
        name = request.json['name']
        surname = request.json.get('surname')
        password = request.json['password']
        email = request.json['email']
        data = [
            current_app.blueprints['user'].controllers.UserController.register_user(name=name, surname=surname,
                                                                                    password=password, email=email),
        ]
        status_code = 201 if None in data else 409
        print(data)
        return self._get_response(data, status_code=status_code)


class LoginView(BaseView):
    def post(self):
        try:
            user_data = LoginSchema().load(data=request.json)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)

        session_id = current_app.blueprints['user'].controllers.LoginController.login(data=user_data)
        response = self._get_response(data=list())
        response.headers['Authorization'] = session_id
        return response
