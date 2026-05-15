import os
import tomllib
import logging
from pathlib import Path
from typing import Optional
from verger.core.config.schema import VergerConfig

logger = logging.getLogger(__name__)

# This will hold the loaded configuration singleton
_config: Optional[VergerConfig] = None


def get_config() -> VergerConfig:
    """Returns the loaded configuration. Raises error if not loaded."""
    if _config is None:
        raise RuntimeError(
            "Verger configuration has not been loaded. Call load_config() first."
        )
    return _config


def load_config(root_dir: Optional[Path] = None) -> VergerConfig:
    """
    Finds and parses the configuration file.
    Priority:
    1. VERGER_CONFIG environment variable
    2. pyproject.toml [tool.verger] in CWD
    3. verger.toml in CWD
    """
    global _config

    # 1. Check for Environment Variable Override
    if env_config_path := os.getenv("VERGER_CONFIG"):
        path = Path(env_config_path)
        if path.exists():
            _config = _load_from_file(path)
            logger.debug(f"Loaded configuration from environment override: {path}")
            return _config
        else:
            logger.error(f"VERGER_CONFIG points to non-existent file: {path}")

    root = root_dir or Path.cwd()

    # 2. Check pyproject.toml
    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        config_data = _parse_pyproject(pyproject_path)
        if config_data:
            _config = VergerConfig(**config_data)
            logger.debug(f"Loaded configuration from {pyproject_path}")
            return _config

    # 3. Check verger.toml
    verger_toml_path = root / "verger.toml"
    if verger_toml_path.exists():
        _config = _load_from_file(verger_toml_path)
        logger.debug(f"Loaded configuration from {verger_toml_path}")
        return _config

    # Default: Empty config
    logger.warning("No configuration file found. Using default settings.")
    _config = VergerConfig()
    return _config


def _load_from_file(path: Path) -> VergerConfig:
    """Helper to load a raw TOML file into VergerConfig."""
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return VergerConfig(**data)


def _parse_pyproject(path: Path) -> Optional[dict]:
    """Helper to extract [tool.verger] from pyproject.toml."""
    with open(path, "rb") as f:
        data = tomllib.load(f)
    return data.get("tool", {}).get("verger")
