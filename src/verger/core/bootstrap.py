from verger.core.plugins import load_plugins
from verger.core.config.loader import load_config
from verger.core.config.env import load_env


def setup_app():
    """
    Initializes the core logic by loading configuration, environment variables,
    and discovering plugins.
    """
    # Step 1: Load configuration (finds pyproject.toml in CWD)
    load_config()

    # Step 2: Load environment variables (based on env_file in config)
    load_env()

    # Step 3: Discover plugins
    load_plugins()
