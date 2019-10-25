from helper_classes.email_builder.build_email import build_email
from flask import current_app
import celery


class UserController:
    @classmethod
    def register_user(cls, name, email, password, surname=None):

        user = current_app.models.User.get_user_by_email(email=email)

        if user is None:
            user = current_app.models.User.create_user(
                name=name, email=email,
                password=password, surname=surname
            )
            cls.setup_registration_otc(user)
            return 'user created'

        if user.is_active:
            return 'user is registered'
        if current_app.blueprints['otc'].controllers.OTCController\
            .is_otc_valid(user.uuid):
            return 'uuid is valid'

        user.delete_user()
        user = current_app.models.User.create_user(
            name=name, email=email,
            password=password, surname=surname
        )
        cls.setup_registration_otc(user)
        return 'uuid updated'


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
