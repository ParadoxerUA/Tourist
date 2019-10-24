from apps.user_app.models import User, ValidationError
from helper_classes.email_builder.build_email import build_email
import requests
from flask import current_app


class UserController:
    @classmethod
    def register_user(cls, name, email, password, surname=None):
        user = User.get_user(email=email)

        if user is None:
            user = User.create_user(
                name=name, email=email,
                password=password, surname=surname
            )
            cls.setup_registration_otc(user)
            return 'user created'

        if user.is_active:
            user.delete_user()
            User.create_user(
                name=name, email=email,
                password=password, surname=surname
            )
            return 'user is registered'
        if current_app.blueprints['otc'].controllers.OTCController\
            .is_otc_available(user.get_uuid()):
            return 'uuid is valid'

        cls.setup_registration_otc(user)
        return 'uuid updated'

    @classmethod
    def activate_user(cls, user_id):
        user = User.get_user(user_id=user_id)
        user.activate_user()

    @classmethod
    def change_capacity(cls, user_id, capacity):
        user = User.get_user(user_id=user_id)
        user.change_capacity(capacity)

    @classmethod
    def setup_registration_otc(cls, user):
        uuid = current_app.blueprints['otc'].controllers.\
            OTCController.get_registration_uuid()
        user.set_uuid(uuid)
        em_type = 'email_confirmation'
        content = {'username': user.name, 'uuid': uuid}
        email_data = build_email(user.email, em_type, **content)
        url = 'http://localhost:5001/send_email'
        response = requests.post(url, json=email_data)
        print(response.json)
