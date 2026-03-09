class TreadmillError(Exception):
    """Base exception for pymvtreadmill."""


class TreadmillConnectionError(TreadmillError):
    """Raised when connection fails or is lost."""
