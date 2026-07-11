class AuthenticationError(Exception):
    """Base exception for authentication errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""


class InvalidTokenError(AuthenticationError):
    """Raised when a JWT is invalid."""


class ExpiredTokenError(AuthenticationError):
    """Raised when a JWT has expired."""


class EmailAlreadyExistsError(AuthenticationError):
    """Raised when a customer registers with an existing email."""
