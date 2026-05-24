from unittest.mock import patch

from verger.core.bootstrap import setup_app


def test_setup_app(mock_user_project):
    """Test that setup_app triggers the core initialization sequence."""
    with (
        patch("verger.core.bootstrap.load_config") as mock_load_config,
        patch("verger.core.bootstrap.load_env") as mock_load_env,
        patch("verger.core.bootstrap.load_plugins") as mock_load_plugins,
    ):
        setup_app()

        mock_load_config.assert_called_once()
        mock_load_env.assert_called_once()
        mock_load_plugins.assert_called_once()
