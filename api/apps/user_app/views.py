from helper_classes.base_view import BaseView
from flask import current_app, request


class UserRegistrationView(BaseView):
    def post(self):
        name = request.form['name']
        surname = request.form.get('surname')
        password = request.form['password']
        email = request.form['email']
        data = [
            current_app.blueprints['user'].controllers.UserController.register_user(name=name, surname=surname,
                                                                                    password=password, email=email),
        ]
        status_code = 201 if None in data else 409
        print(data)
        return self._get_response(data, status_code=status_code)



