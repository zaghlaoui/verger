from verger.core.exceptions import VergerConfigurationError, VergerError, VergerResolutionError


def test_exception_hierarchy():
    """Test that all custom exceptions inherit from VergerError."""
    assert issubclass(VergerConfigurationError, VergerError)
    assert issubclass(VergerResolutionError, VergerError)
    assert isinstance(VergerError(), Exception)
