"""Custom exceptions for the Verger framework."""


class VergerError(Exception):
    """Base exception for all Verger-related errors."""

    pass


class VergerConfigurationError(VergerError):
    """Raised when configuration loading fails or is invalid."""

    pass


class VergerResolutionError(VergerError):
    """Raised when an object (model, prompt, tool) cannot be resolved to a Verger adapter."""

    pass
