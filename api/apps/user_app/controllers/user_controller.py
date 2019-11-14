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
            raise ValidationError('User is already registered')
        if user.is_uuid_valid():
            return 'uuid is valid'

        user.delete_user()
        user = current_app.models.User.create_user(
            name=name, email=email,
            password=password, surname=surname
        )
        cls.setup_registration_otc(user)
        return 'user uuid updated'


    @classmethod
    def activate_user(cls, user_id):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        user.activate_user()

    @classmethod
    def change_capacity(cls, user_id, capacity):
        user = current_app.models.get_user_by_id(user_id=user_id)
        user.change_capacity(capacity)

    @classmethod
    def setup_registration_otc(cls, user):
        celery_app = celery.Celery(
            current_app.config['CELERY_APP_NAME'],
            broker=current_app.config['CELERY_BROKER_URL'])
        uuid = current_app.blueprints['otc'].controllers.\
            OTCController.get_registration_uuid()
        user.set_uuid(uuid)
        em_type = 'email_confirmation'
        content = {'username': user.name, 'uuid': uuid}
        email_data = build_email(user.email, em_type, **content)
        celery_app.send_task('app.async_email', kwargs={'data': email_data})

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

    @classmethod
    def change_password(cls, user_id, new_password, old_password=None):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        if not user.password_is_set() or (old_password and user.check_password(old_password)):
            user.set_password(new_password)
            return 'Your password was updated'
        else:
            raise ValidationError('Wrong password')


            
