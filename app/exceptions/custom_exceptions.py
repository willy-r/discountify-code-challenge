class CouponNotFoundException(Exception):
    pass


class CouponAlreadyExistsException(Exception):
    pass


class CouponRulesException(Exception):
    pass

class CouponExpiredException(CouponRulesException):
    pass


class CouponMaxUtilizationsExceededException(CouponRulesException):
    pass

class CouponMinPurchaseValueExceededException(CouponRulesException):
    pass


class CouponFirstPurchaseException(CouponRulesException):
    pass
