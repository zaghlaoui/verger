"""Environment variable management and .env loading."""

import logging
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

from verger.core.config.loader import get_config

logger = logging.getLogger(__name__)


def load_env(root_dir: Path | None = None) -> list[str]:
    """
    Loads environment variables from the file specified in the configuration.
    Defaults to '.env' in the current working directory.

    Returns:
        A list of the keys that were loaded from the .env file.
    """
    try:
        config = get_config()
        env_file_name = config.env_file or ".env"

        root = root_dir or Path.cwd()
        env_path = root / env_file_name

        if env_path.exists():
            # Use load_dotenv for side-effects and dotenv_values to get the keys
            load_dotenv(env_path)
            logger.debug(f"Loaded environment variables from {env_path}")
            return list(dotenv_values(env_path).keys())
        else:
            if config.env_file != ".env":
                # Only warn if the user explicitly specified a file that's missing
                logger.warning(f"Specified env_file not found: {env_path}")

    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")

    return []
