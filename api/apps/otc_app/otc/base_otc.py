from .otc_exceptions import OTCNoneError

class BaseOTC:
    def __init__(self, otc_type):
        self._otc_type = otc_type
        self._code = None

    def get_otc(self):
        if self._code:
            return self._code
        raise OTCNoneError()

    def get_otc_type(self):
        return self._otc_type

    def create_otc(self):
        pass
