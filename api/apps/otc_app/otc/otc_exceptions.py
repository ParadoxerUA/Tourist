class OTCBaseException(Exception):
    pass


class OTCTypeError(OTCBaseException):
    pass


class OTCUnavailableError(OTCBaseException):
    pass
