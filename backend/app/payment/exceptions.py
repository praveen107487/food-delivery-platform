class PaymentException(Exception):
    """Base exception for all payment-related errors."""


class PaymentNotFoundException(PaymentException):
    """Raised when a payment is not found."""


class PaymentNotEligibleException(PaymentException):
    """Raised when a payment cannot be created for an order."""


class PaymentAlreadySuccessfulException(PaymentException):
    """Raised when an order already has a successful payment."""


class PaymentAccessDeniedException(PaymentException):
    """Raised when a customer attempts to access another customer's payment."""


class PaymentAmountMismatchException(PaymentException):
    """Raised when the payment amount does not match the order total."""


class PaymentRetryNotAllowedException(PaymentException):
    """Raised when a payment retry is not allowed."""


class PaymentVerificationFailedException(PaymentException):
    """Raised when payment verification fails."""


class InvalidPaymentStatusTransitionException(PaymentException):
    """Raised when a payment status transition is invalid."""


class UnsupportedPaymentMethodException(PaymentException):
    """Raised when the payment method is not supported."""
