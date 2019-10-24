from apps.otc_app.otc import registration_otc
from apps.otc_app.otc.otc_exceptions import *
import redis


class OTCController():
    @classmethod
    def create_OTC_instance(cls, otc_type):
        if otc_type == 'user_registration':
            return registration_otc.RegistrationOTC()
        else:
            raise OTCTypeError()

    @classmethod
    def get_otc_type(cls, otc):
        with redis.Redis() as r:
            otc_type = r.get(otc)

        if otc_type is None:
            raise OTCUnavailableError()

        return otc_type.decode('utf8')

    @classmethod
    def is_otc_available(cls, otc):
        try:
            print(cls.get_otc_type(otc))
            return True
        except OTCUnavailableError:
            return False

    @classmethod
    def get_registration_uuid(cls):
        otc = registration_otc.RegistrationOTC()
        otc.setup_otc()
        return otc.get_otc()
