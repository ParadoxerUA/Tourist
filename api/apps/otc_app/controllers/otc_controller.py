from apps.otc_app.otc import registration_otc
from apps.otc_app.otc.otc_exceptions import *
from flask import current_app
from datetime import datetime
import redis


class OtcController():
    redis_client = None

    @classmethod
    def handle_uuid(cls, uuid):
        cls.redis_client = redis.Redis()
        otc_type = cls.redis_client.get(uuid)
    
        if otc_type == False:
            raise OtcNoneError('specified uuid does not exist')

        otc_type = otc_type.decode('utf-8')
        if otc_type == 'user_registration':
            return cls._handle_user_registration_uuid(uuid)

        raise OtcTypeError

    @classmethod
    def _handle_user_registration_uuid(cls, uuid):
        try:
            action_result = cls._activate_user(uuid)
            cls.redis_client.delete(uuid)
            return action_result
        except OtcOutdatedError:
            return 'uuid outdated'

    @classmethod
    def create_registration_uuid(cls):
        otc = registration_otc.RegistrationOtc()
        otc.create_otc()
        otc.add_otc_to_redis()
        return otc.get_otc()

    @classmethod
    def _activate_user(cls, uuid):
        user = current_app.models.User.get_user_by_uuid(uuid)
        if user.is_active:
            return 'user already activated'
        if user.is_uuid_valid():
            user.activate_user()
            return 'user activated'
        raise OtcOutdatedError
