class VergerError(Exception):
    """Base exception for all Verger-related errors."""

    pass


class VergerConfigurationError(VergerError):
    """Raised when configuration loading fails or is invalid."""

    pass
