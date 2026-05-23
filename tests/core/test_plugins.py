from unittest.mock import MagicMock, patch

from verger.core.plugins import load_plugins


def test_load_plugins_error_handling(caplog):
    """Test that plugin loading handles errors gracefully (covering except blocks)."""
    # Mock pkgutil.iter_modules to return some module names
    # Mock importlib.import_module to raise an exception for those modules

    with patch("pkgutil.iter_modules") as mock_iter:
        mock_iter.return_value = [
            (None, "broken_model", False),
            (None, "broken_prompt", False),
            (None, "broken_tool", False),
        ]

        with patch("importlib.import_module") as mock_import:
            mock_import.side_effect = Exception("Import error")

            with caplog.at_level("ERROR"):
                load_plugins()

            assert "Failed to load model adapter" in caplog.text
            assert "Failed to load prompt adapter" in caplog.text
            assert "Failed to load tool adapter" in caplog.text


def test_load_plugins_no_resolver(caplog):
    """Test modules that don't have a get_resolver function."""
    with patch("pkgutil.iter_modules") as mock_iter:
        mock_iter.return_value = [(None, "no_resolver_mod", False)]

        with patch("importlib.import_module") as mock_import:
            mock_module = MagicMock()
            del mock_module.get_resolver
            mock_import.return_value = mock_module

            load_plugins()
            # Should not log error, just skip it
            assert "Failed to load" not in caplog.text
