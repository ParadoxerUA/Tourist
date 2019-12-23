from .otc_exceptions import OtcNoneError, OtcInsertionError
import redis
from flask import current_app

class BaseOtc:
    def __init__(self, otc_type):
        self._otc_type = otc_type
        self._code = None

    def get_otc(self):
        if self._code:
            return self._code
        raise OtcNoneError

    def get_otc_type(self):
        return self._otc_type

    def add_otc_to_redis(self):
        if not self._code:
            raise OtcNoneError
        with create_redis_tmp() as redis_client:
            res = redis_client.set(self._code, self._otc_type)
            if res == False:
                raise OtcInsertionError("redis insertion failed")

    def create_otc(self):
        raise NotImplementedError

def create_redis_tmp():
    broker_url = current_app.config['CELERY_BROKER_URL']
    slashes_index = broker_url.index('//')
    semicolon_index = broker_url.index(':', slashes_index)
    last_slash_index = broker_url.index('/', semicolon_index)

    host = broker_url[slashes_index + 2:semicolon_index]
    port = broker_url[semicolon_index + 1:last_slash_index]
    db = broker_url[last_slash_index + 1:]
    return redis.Redis(host=host, port=port, db=db)
