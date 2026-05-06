# core/provider_loader.py

import importlib
from pathlib import Path
from app.logger.logging import get_logger

logger = get_logger(__name__)
PROVIDERS = {}


def load_providers():
    logger.info("Starting provider loading...")
    app_root = Path(__file__).resolve().parent.parent
    base_path = app_root / "providers"

    if not base_path.exists():
        logger.error(f"Provider base path not found: {base_path}")
        return

    folders = [p for p in base_path.iterdir() if p.is_dir() and not p.name.startswith("__")]
    logger.debug(f"Found {len(folders)} provider folders: {[p.name for p in folders]}")

    for folder in folders:
        try:
            logger.debug(f"Loading provider from folder: {folder.name}")
            module = importlib.import_module(f"app.providers.{folder.name}.provider")
            cls = getattr(module, "Provider")

            instance = cls()
            provider_name = instance.name()
            PROVIDERS[provider_name] = instance
            logger.info(f"Provider loaded successfully: {provider_name}")

        except ImportError as e:
            logger.warning(f"Provider import error for {folder.name}: {str(e)}")
        except AttributeError as e:
            logger.warning(f"Provider class not found in {folder.name}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error loading provider {folder.name}: {str(e)}", exc_info=True)
    
    logger.info(f"Provider loading completed. Loaded {len(PROVIDERS)} providers: {list(PROVIDERS.keys())}")