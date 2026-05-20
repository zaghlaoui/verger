"""Model registration and adapter interfaces."""

from .base import ModelResolver, VergerModel
from .model_registry import model_registry

__all__ = ["model_registry", "VergerModel", "ModelResolver"]
