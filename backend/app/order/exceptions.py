class OrderError(Exception):
    """Base exception for order-related errors."""


class OrderNotFoundError(OrderError):
    """Raised when the requested order does not exist."""


class ActiveCartNotFoundError(OrderError):
    """Raised when the customer has no active cart for checkout."""


class EmptyCartError(OrderError):
    """Raised when attempting to checkout an empty cart."""


class OrderAccessDeniedError(OrderError):
    """Raised when a customer attempts to access another customer's order."""


class CheckoutValidationError(OrderError):
    """Raised when checkout validation fails."""
