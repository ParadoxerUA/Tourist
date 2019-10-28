from apps.otc_app.otc import registration_otc
from apps.otc_app.otc.otc_exceptions import *
from flask import current_app
from datetime import datetime


class OTCController():
    @classmethod
    def handle_uuid(cls, uuid, otc_type):
        if otc_type == 'user_registration':
            try:
                return cls._activate_user(uuid)
            except OTCOutdatedError:
                return 'uuid outdated'
        else:
            raise OTCTypeError()

    @classmethod
    def get_registration_uuid(cls):
        otc = registration_otc.RegistrationOTC()
        otc.create_otc()
        return otc.get_otc()

    @classmethod
    def _activate_user(cls, uuid):
        user = current_app.models.User.get_user_by_uuid(uuid)
        if user.is_active:
            return 'user already activated'
        if user.is_uuid_valid():
            user.activate_user()
            return 'user activated'
        raise OTCOutdatedError()
