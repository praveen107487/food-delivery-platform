class CartNotFoundException(Exception):
    """Raised when the customer's active cart does not exist."""


class CartItemNotFoundException(Exception):
    """Raised when the requested cart item does not exist."""


class CartRestaurantMismatchException(Exception):
    """Raised when attempting to add menu items from another restaurant."""


class MenuItemUnavailableException(Exception):
    """Raised when the menu item does not exist or is unavailable."""
