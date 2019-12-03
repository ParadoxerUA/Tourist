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

    # tofix
    @classmethod
    def register_user(cls, name, email, password, surname=None):
        user = current_app.models.User.get_user_by_email(email=email)
        if user is None:
            user = current_app.models.User.create_user(
                name=name, email=email,
                password=password, surname=surname,
                avatar='http://localhost:5000/static/images/user_avatar.png'
            )
            cls._setup_registration_otc(user)
            return 'user created', 201

        if user.is_active:
            return 'User is already registered', 401
        if user.is_uuid_valid():
            return 'uuid is valid', 402

        user.delete_user()
        # tofix
        user = current_app.models.User.create_user(
            name=name, email=email,
            password=password, surname=surname
        )
        cls._setup_registration_otc(user)
        return 'user uuid updated', 403

    # need to OTC work
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
    def update_user(cls, data):
        current_app.models.User.update_user(data, user_id=g.user_id)
        return 'User was successfully updated', 200

    @classmethod
    def _setup_registration_otc(cls, user):
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

    @classmethod
    def change_password(cls, new_password, old_password=None):
        user = cls._get_user(g.user_id)
        if (not user.password_is_set()) or (old_password and user.check_password(old_password)):
            user.set_password(new_password)
            return 'Your password was updated', 200
        else:
            return 'Wrong password', 401

    @classmethod
    def delete_user_from_trip(cls, trip_id, user_to_delete):
        trip = current_app.models.Trip.get_trip_by_id(trip_id=trip_id)
        if (user_to_delete != g.user_id) and (g.user_id != trip.admin_id):
            return 'You have no rights', 401
        user = cls._get_user(user_to_delete)
        return trip.delete_user(user), 201

    @classmethod
    def get_user_data(cls, fields, *, trip_id=None):
        user = cls._get_user(g.user_id)
        if trip_id:
            try:
                trip_id = int(trip_id)
            except TypeError:
                'trip_id should be int', 402
        user_data = user.get_fields(fields, trip_id=trip_id)
        return user_data, 201

