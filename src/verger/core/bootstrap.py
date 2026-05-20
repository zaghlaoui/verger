"""Initialization logic for setting up the Verger core."""

import os
import sys

from verger.core.config.env import load_env
from verger.core.config.loader import load_config
from verger.core.plugins import load_plugins


def setup_app():
    """
    Initializes the core logic by loading configuration, environment variables,
    and discovering plugins.
    """
    # Inject Current Working Directory into sys.path so we can import user modules
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.insert(0, cwd)

    # Step 1: Load configuration
    load_config()

    # Step 2: Load environment variables (based on env_file in config)
    load_env()

    # Step 3: Discover plugins
    load_plugins()
