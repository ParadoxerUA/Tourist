from helper_classes.email_builder.build_email import build_email
from marshmallow import ValidationError
from flask import current_app
import celery


class UserController:
    @classmethod
    def register_user(cls, name, email, password, surname=None):

        user = current_app.models.User.get_user_by_email(email=email)

        if user is None:
            user = current_app.models.User.create_user(
                name=name, email=email,
                password=password, surname=surname,
                avatar='http://localhost:5000/static/images/user_avatar.png'
            )
            cls.setup_registration_otc(user)
            return 'user created'

        if user.is_active:
            return 'User is already registered'
        if user.is_uuid_valid():
            return 'uuid is valid'

        user.delete_user()
        # tofix
        user = current_app.models.User.create_user(
            name=name, email=email,
            password=password, surname=surname
        )
        cls.setup_registration_otc(user)
        return 'user uuid updated'


    @classmethod
    def activate_user(cls, user_uuid):
        user = current_app.models.User.get_user_by_uuid(user_uuid)

        if user.is_active:
            return 'user already activated', 409
        if user.is_uuid_valid():
            user.activate_user()
            return 'user activated', 200
        return 'uuid outdated', 409

    @classmethod
    def change_capacity(cls, user_id, capacity):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        user.change_capacity(capacity)

        return user.capacity

    @classmethod
    def setup_registration_otc(cls, user):
        celery_app = celery.Celery(
            current_app.config['CELERY_APP_NAME'],
            broker=current_app.config['CELERY_BROKER_URL']
        )
        uuid = current_app.blueprints['otc'].controllers.\
            OtcController.create_registration_uuid()
        user.set_uuid(uuid)
        em_type = 'email_confirmation'
        content = {'username': user.name, 'uuid': uuid}
        email_data = build_email(user.email, em_type, **content)
        celery_app.send_task('app.async_email', kwargs = email_data)

    @staticmethod
    def get_user_profile(user_id):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        user_profile_data = {
            'user_id': user_id,
            'avatar': user.avatar,
            'name': user.name,
            'surname': user.surname,
            'email': user.email,
            'capacity': user.capacity
        }
        return user_profile_data
