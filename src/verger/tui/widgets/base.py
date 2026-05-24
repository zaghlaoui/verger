"""Base classes and reusable widgets for the Verger TUI."""

from typing import Any

from textual.containers import Vertical

from verger.core.config.schema import VergerConfig
from verger.core.engine import ExecutionEngine


class VergerTUIComponent(Vertical):
    """Base component for Verger TUI with shared properties."""

    def __init__(self, app_ref: Any, **kwargs: Any):
        super().__init__(**kwargs)
        self.app_ref = app_ref

    @property
    def engine(self) -> ExecutionEngine:
        """Access the execution engine from the parent app."""
        return self.app_ref.engine

    @property
    def config(self) -> VergerConfig:
        """Access the configuration from the parent app."""
        return self.app_ref.config
