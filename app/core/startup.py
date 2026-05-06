from app.core.provider_loader import PROVIDERS
from app.core.model_registry import model_registry
from app.logger.logging import get_logger

logger = get_logger(__name__)

async def preload_all_models():
    logger.info("Starting model preload process...")
    
    try:
        # group models by provider
        provider_map = {}

        for model_name, config in model_registry.models.items():
            provider = config["provider"]

            if provider not in provider_map:
                provider_map[provider] = []

            provider_map[provider].append(config)
        
        logger.debug(f"Models grouped by provider: {list(provider_map.keys())}")

        # call preload on each provider (if available)
        for provider_name, models in provider_map.items():
            logger.debug(f"Processing {len(models)} models for provider: {provider_name}")
            provider = PROVIDERS.get(provider_name)

            if not provider:
                logger.error(f"Provider not found: {provider_name}")
                continue

            if hasattr(provider, "preload_models"):
                logger.info(f"Preloading {len(models)} models for provider: {provider_name}")
                try:
                    await provider.preload_models(models)
                    logger.info(f"Successfully preloaded models for provider: {provider_name}")
                except Exception as e:
                    logger.error(f"Error preloading models for {provider_name}: {str(e)}", exc_info=True)
                    raise
            else:
                logger.warning(f"Provider {provider_name} does not support model preloading")
        
        logger.info("Model preload process completed successfully")
    except Exception as e:
        logger.error(f"Critical error during model preloading: {str(e)}", exc_info=True)
        raise