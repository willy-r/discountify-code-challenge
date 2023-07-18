class CouponNotFoundException(Exception):
    pass


class CouponAlreadyExistsException(Exception):
    pass


class CouponRulesException(Exception):
    pass

class CouponExpiredException(CouponRulesException):
    pass


class CouponMaxUtilizationException(CouponRulesException):
    pass

class CouponMinPurchaseValueException(CouponRulesException):
    pass


class CouponOnlyFirstPurchaseException(CouponRulesException):
    pass
