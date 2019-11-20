from apps.otc_app.otc import registration_otc, trip_link_otc
from apps.otc_app.otc.otc_exceptions import *
from flask import current_app
from datetime import datetime
import redis


class OtcController():
    @classmethod
    def handle_uuid(cls, uuid):
        redis_client = redis.Redis()
        print(uuid)
        otc_type = redis_client.get(uuid)
    
        if otc_type is None:
            raise OtcNoneError('specified uuid does not exist')
        otc_type = otc_type.decode('utf-8')

        if otc_type == 'user_registration':
            action_result = current_app.blueprints['user'].controllers.UserController.activate_user(uuid)
            redis_client.delete(uuid)
            return action_result
        if otc_type == 'trip_link':
            return current_app.blueprints['trip'].controllers.TripController.user_to_trip(uuid)

        raise OtcTypeError

    @classmethod
    def create_registration_uuid(cls):
        otc = registration_otc.RegistrationOtc()
        return cls._setup_otc(otc)

    @classmethod
    def create_trip_link_uuid(cls):
        otc = trip_link_otc.TripLinkOtc()
        return cls._setup_otc(otc)

    @classmethod
    def _setup_otc(cls, otc):
        otc.create_otc()
        otc.add_otc_to_redis()
        return otc.get_otc()
