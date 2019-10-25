class OTCBaseException(Exception):
    pass


class OTCTypeError(OTCBaseException):
    pass


class OTCOutdatedError(OTCBaseException):
    pass

class OTCNoneError(OTCBaseException):
    pass
