class PaymentException(Exception):
    """Base exception for all payment-related errors."""


class PaymentNotFoundException(PaymentException):
    """Raised when a payment is not found."""


class PaymentAlreadySuccessfulException(PaymentException):
    """Raised when an order already has a successful payment."""


class PaymentAmountMismatchException(PaymentException):
    """Raised when the payment amount does not match the order total."""


class PaymentRetryNotAllowedException(PaymentException):
    """Raised when a payment retry is not allowed."""


class InvalidPaymentStatusTransitionException(PaymentException):
    """Raised when a payment status transition is invalid."""


class UnsupportedPaymentMethodException(PaymentException):
    """Raised when the payment method is not supported."""
