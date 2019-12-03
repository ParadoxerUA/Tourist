from helper_classes.email_builder.build_email import build_email
from marshmallow import ValidationError
from flask import current_app, send_from_directory, g
import uuid
import celery
import os
from pathlib import Path
print("Directory Path:", Path().absolute())


class UserController:
    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

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
    def update_user(cls, user_id, data):
        current_app.models.User.update_user(data, user_id=user_id)
        return 'User was successfully updated', 200

    @classmethod
    def change_user_data(cls, user_id, name, surname, capacity):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        user.change_public_fields(name, surname, capacity)

    @classmethod
    def save_user_avatar(cls, user_id, avatar):
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        image_store_url = 'http://localhost:5000/api/user/v1/user/avatar'
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        prefix = uuid.uuid4()
        file_format = avatar.filename[avatar.filename.rindex('.')+1:]
        current_folder = Path().absolute()
        full_path = os.path.join(str(current_folder) + current_app.config['UPLOAD_FOLDER'])
        if not os.path.isdir(full_path):
            os.makedirs(full_path)
        if file_format in allowed_extensions:
            old_user_avatar_url = user.avatar
            avatar_file_name = "{}-{}.{}".format(prefix, user_id, file_format)
            avatar.save(full_path+avatar_file_name)
            user.change_avatar_url('{}?avatar={}'.format(image_store_url, avatar_file_name))
            if old_user_avatar_url.find('?') != -1:
                old_avatar_name = old_user_avatar_url[old_user_avatar_url.rindex('=') + 1:]
                cls.delete_old_avatar_file(old_avatar_name)
        else:
            raise ValidationError('Wrong avatar extension')

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
    def get_profile(user_id):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        return user.get_public_data()

    @classmethod
    def change_password(cls, user_id, new_password, old_password=None):
        user = current_app.models.User.get_user_by_id(user_id=user_id)
        if (not user.password_is_set()) or (old_password and user.check_password(old_password)):
            user.set_password(new_password)
            return 'Your password was updated', 200
        else:
            return 'Wrong password', 401

    @classmethod
    def delete_user_from_trip(cls, trip_id, user_to_delete):
        trip = current_app.models.Trip.get_trip_by_id(trip_id=trip_id)
        if (user_to_delete != g.user_id) and (g.user_id != trip.admin_id):
            return None
        user = cls._get_user(user_to_delete)
        return trip.delete_user(user)

    @classmethod
    def get_trips(cls):
        user = cls._get_user(g.user_id)
        return user.get_trips(), 201

    @classmethod
    def get_roles(cls):
        user = cls._get_user(g.user_id)
        return user.get_roles(), 201

    @staticmethod
    def delete_old_avatar_file(avatar_file_name):
        full_path = os.path.join(str(Path().absolute())+current_app.config['UPLOAD_FOLDER']+avatar_file_name)
        print('Detele ', full_path, os.path.isfile(full_path))
        if os.path.isfile(full_path):
            os.remove(full_path)

    @staticmethod
    def get_user_avatar_path():
        full_path = os.path.join(str(Path().absolute()) + current_app.config['UPLOAD_FOLDER'])
        return full_path


