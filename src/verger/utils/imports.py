import importlib
from typing import Any


def import_reference(ref: str) -> Any:
    """
    Dynamically imports a module and extracts an attribute based on a reference string.

    Args:
        ref: The reference string, formatted as 'module.path:attribute_name'

    Returns:
        The extracted Python object.

    Raises:
        ValueError: If the format is invalid.
        ImportError: If the module cannot be imported.
        AttributeError: If the attribute does not exist in the module.
    """
    if not isinstance(ref, str) or ":" not in ref:
        raise ValueError(
            f"Invalid reference format: '{ref}'. Expected 'module.path:attribute_name'."
        )

    module_path, attr_name = ref.split(":", 1)

    try:
        module = importlib.import_module(module_path)
    except ImportError as e:
        raise ImportError(f"Could not import module '{module_path}' for reference '{ref}'.") from e

    try:
        return getattr(module, attr_name)
    except AttributeError as e:
        raise AttributeError(f"Module '{module_path}' has no attribute '{attr_name}'.") from e
