import yaml
from typing import Dict
from app.logger.logging import get_logger

logger = get_logger(__name__)

class ModelRegistry:

    def __init__(self):
        self.models: Dict[str, dict] = {}

    def load_from_yaml(self, path: str):
        logger.debug(f"Loading model registry from {path}")
        try:
            with open(path, "r") as f:
                data = yaml.safe_load(f)

            for m in data.get("models", []):
                self.models[m["name"]] = m
                logger.debug(f"Registered model: {m['name']} with provider: {m.get('provider', 'unknown')}")
            
            logger.info(f"Model registry loaded successfully with {len(self.models)} models")
        except FileNotFoundError:
            logger.error(f"Model registry file not found: {path}")
            raise
        except Exception as e:
            logger.error(f"Error loading model registry from {path}: {str(e)}", exc_info=True)
            raise

    def get(self, name: str):
        logger.debug(f"Fetching model configuration for: {name}")
        model = self.models.get(name)
        if not model:
            logger.warning(f"Model not found in registry: {name}")
        return model

    def list_models(self):
        logger.debug(f"Listing all {len(self.models)} registered models")
        return list(self.models.keys())


model_registry = ModelRegistry()