from .otc_exceptions import OTCNoneError
import redis

class BaseOTC:
    def __init__(self, otc_type):
        self._otc_type = otc_type
        self._code = None

    def get_otc(self):
        if self._code:
            return self._code
        raise OTCNoneError

    def get_otc_type(self):
        return self._otc_type

    def add_otc_to_redis(self):
        if not self._code:
            raise OTCNoneError
        with redis.Redis() as redis_client:
            res = redis_client.set(self._code, self._otc_type)
            if res == False:
                raise Exception("redis insertion failed")

    def create_otc(self):
        raise NotImplementedError
