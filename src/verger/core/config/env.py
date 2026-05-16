import logging
from pathlib import Path

from dotenv import load_dotenv

from verger.core.config.loader import get_config

logger = logging.getLogger(__name__)


def load_env(root_dir: Path | None = None):
    """
    Loads environment variables from the file specified in the configuration.
    Defaults to '.env' in the current working directory.
    """
    try:
        config = get_config()
        env_file_name = config.env_file or ".env"

        root = root_dir or Path.cwd()
        env_path = root / env_file_name

        if env_path.exists():
            load_dotenv(env_path)
            logger.debug(f"Loaded environment variables from {env_path}")
        else:
            if config.env_file != ".env":
                # Only warn if the user explicitly specified a file that's missing
                logger.warning(f"Specified env_file not found: {env_path}")

    except Exception as e:
        logger.error(f"Failed to load environment variables: {e}")
