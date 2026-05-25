"""Modular package for the Verger Prompt Lab."""

from .service import LabService

# Singleton instance to be used across the application
lab_service = LabService()

__all__ = ["LabService", "lab_service"]
