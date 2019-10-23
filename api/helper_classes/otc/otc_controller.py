from . import registration_otc
from .otc_exceptions import *
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
