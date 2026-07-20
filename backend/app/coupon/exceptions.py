class CouponException(Exception):
    """Base exception for coupon module."""


class CouponNotFoundException(CouponException):
    """Raised when the coupon code does not exist."""


class CouponInactiveException(CouponException):
    """Raised when the coupon is inactive."""


class CouponExpiredException(CouponException):
    """Raised when the coupon has expired."""


class CouponNotYetActiveException(CouponException):
    """Raised when the coupon validity has not started."""


class MinimumOrderAmountNotMetException(CouponException):
    """Raised when the cart subtotal is below the minimum order amount."""


class RestaurantCouponMismatchException(CouponException):
    """Raised when a restaurant coupon does not belong to the cart restaurant."""
