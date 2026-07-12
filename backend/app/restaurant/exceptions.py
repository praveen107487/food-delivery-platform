class RestaurantNotFoundException(Exception):
    """Raised when the requested restaurant does not exist."""


class RestaurantSearchValidationException(Exception):
    """Raised when the restaurant search keyword is invalid."""
