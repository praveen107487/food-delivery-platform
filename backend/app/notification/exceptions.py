class NotificationException(Exception):
    """Base exception for notification errors."""


class NotificationNotFoundException(NotificationException):
    """Raised when a notification cannot be found."""


class NotificationOwnershipException(NotificationException):
    """Raised when a customer tries to access another customer's notification."""
