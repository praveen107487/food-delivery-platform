class CustomerException(Exception):
    """Base exception for all customer domain errors."""


class CustomerNotFoundException(CustomerException):
    """Raised when the requested customer does not exist."""


class SavedAddressNotFoundException(CustomerException):
    """Raised when the requested saved address does not exist."""


class AddressOwnershipException(CustomerException):
    """Raised when a customer attempts to access another customer's address."""


class DefaultAddressNotFoundException(CustomerException):
    """Raised when no default address exists for the customer."""
