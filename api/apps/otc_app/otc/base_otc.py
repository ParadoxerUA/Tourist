import redis


class BaseOTC:
    def __init__(self, otc_type):
        self._otc_type = otc_type
        self._code = None

    def setup_otc(self):
        self._code = str(self._create_otc())
        self._insert_to_redis()

    def get_otc(self):
        return self._code 

    def _insert_to_redis(self):
        with redis.Redis() as r:
            r.set(self._code, self._otc_type)

    def _create_otc(self):
        pass
