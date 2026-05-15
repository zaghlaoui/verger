import importlib
import pkgutil
import logging
from verger.core.models.registry import registry as model_registry
from verger.core.prompts.registry import registry as prompt_registry

logger = logging.getLogger(__name__)


def load_plugins():
    """Entry point to load all internal adapters."""
    _register_model_adapters()
    _register_prompt_adapters()


def _register_model_adapters():
    """Automatically loads and registers all model resolvers from the adapters directory."""
    import verger.core.models.adapters as pkg

    for _, name, _ in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        try:
            module = importlib.import_module(name)
            if hasattr(module, "get_resolver"):
                model_registry.register(module.get_resolver())
                logger.debug(f"Registered model resolver from {name}")
        except Exception as e:
            logger.error(f"Failed to load model adapter {name}: {e}")


def _register_prompt_adapters():
    """Automatically loads and registers all prompt resolvers from the adapters directory."""
    import verger.core.prompts.adapters as pkg

    for _, name, _ in pkgutil.iter_modules(pkg.__path__, pkg.__name__ + "."):
        try:
            module = importlib.import_module(name)
            if hasattr(module, "get_resolver"):
                prompt_registry.register(module.get_resolver())
                logger.debug(f"Registered prompt resolver from {name}")
        except Exception as e:
            logger.error(f"Failed to load prompt adapter {name}: {e}")
