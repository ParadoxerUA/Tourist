from apps.otc_app.otc import registration_otc
from apps.otc_app.otc.otc_exceptions import *
from flask import current_app
from datetime import datetime


class OTCController():
    @classmethod
    def create_OTC_instance(cls, otc_type):
        if otc_type == 'user_registration':
            return registration_otc.RegistrationOTC()
        else:
            raise OTCTypeError()

    @classmethod
    def is_otc_valid(cls, otc):
        user = current_app.models.User.get_user_by_uuid(otc)
        datetime_diff = datetime.utcnow() - user.registration_time
        diff_in_hours = datetime_diff.total_seconds() / 3600
        if diff_in_hours > 24:
            return False
        return True

    @classmethod
    def get_registration_uuid(cls):
        otc = registration_otc.RegistrationOTC()
        otc.create_otc()
        return otc.get_otc()
