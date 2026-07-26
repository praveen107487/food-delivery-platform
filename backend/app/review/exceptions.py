class ReviewException(Exception):
    """Base exception for the review module."""


class RestaurantReviewNotFoundException(Exception):
    """Raised when the requested restaurant review does not exist."""


class FoodItemReviewNotFoundException(Exception):
    """Raised when the requested food item review does not exist."""


class RestaurantReviewAlreadyExistsException(Exception):
    """Raised when a restaurant review already exists for the order."""


class FoodItemReviewAlreadyExistsException(Exception):
    """Raised when a food item review already exists for the order item."""


class ReviewOwnershipException(Exception):
    """Raised when a user attempts to modify a review they do not own."""


class OrderNotDeliveredException(Exception):
    """Raised when attempting to review an order that has not been delivered."""


class OrderOwnershipException(Exception):
    """Raised when the order does not belong to the authenticated customer."""


class OrderItemOwnershipException(Exception):
    """Raised when the order item does not belong to the authenticated customer."""


class ReviewImageNotFoundException(Exception):
    """Raised when the requested review image does not exist."""
