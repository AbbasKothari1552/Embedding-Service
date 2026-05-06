# engine/embedding_engine.py

from app.core.provider_loader import PROVIDERS
from app.logger.logging import get_logger

logger = get_logger(__name__)

class EmbeddingEngine:

    async def embed(self, provider: str, model: str, input_data):
        logger.debug(f"Embedding request - provider: {provider}, model: {model}, input type: {type(input_data).__name__}")
        
        try:
            if provider not in PROVIDERS:
                logger.error(f"Provider not found: {provider}. Available providers: {list(PROVIDERS.keys())}")
                raise ValueError(f"Provider '{provider}' not found")

            inputs = input_data if isinstance(input_data, list) else [input_data]
            logger.debug(f"Processing {len(inputs)} input(s) with provider: {provider}")

            provider_instance = PROVIDERS[provider]
            embeddings = await provider_instance.embed(model, inputs)
            
            logger.info(f"Successfully generated embeddings using {provider}/{model}")
            return embeddings
        except ValueError as e:
            logger.error(f"Validation error in embedding: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during embedding: {str(e)}", exc_info=True)
            raise