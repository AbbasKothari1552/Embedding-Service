import asyncio
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer

from app.providers.base import EmbeddingProvider
from app.logger.logging import get_logger

logger = get_logger(__name__)

class Provider(EmbeddingProvider):

    def __init__(self):
        logger.debug("Initializing local embedding provider")
        self.models = {}
        self.executor = ThreadPoolExecutor()
        logger.info("Local provider initialized")

    def name(self):
        return "local"

    async def load_model(self, model_name: str, path: str):
        logger.info(f"Loading model '{model_name}' from {path}")
        try:
            loop = asyncio.get_event_loop()

            model = await loop.run_in_executor(
                self.executor,
                SentenceTransformer,
                path
            )

            self.models[model_name] = model
            logger.info(f"Model '{model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model '{model_name}' from {path}: {str(e)}", exc_info=True)
            raise

    async def preload_models(self, model_configs: list[dict]):
        logger.info(f"Starting preload of {len(model_configs)} models")
        tasks = []

        for m in model_configs:
            logger.debug(f"Scheduling preload for model: {m.get('name', 'unknown')}")
            tasks.append(self.load_model(m["name"], m["path"]))

        try:
            await asyncio.gather(*tasks)
            logger.info(f"Successfully preloaded all {len(model_configs)} models")
        except Exception as e:
            logger.error(f"Error during model preloading: {str(e)}", exc_info=True)
            raise

    async def embed(self, model: str, inputs: list[str]) -> list[list[float]]:
        logger.debug(f"Embedding request with model '{model}' and {len(inputs)} input(s)")
        m = self.models.get(model)

        if not m:
            logger.error(f"Model '{model}' not loaded. Available models: {list(self.models.keys())}")
            raise ValueError(f"Model '{model}' not loaded")

        try:
            loop = asyncio.get_event_loop()
            logger.debug(f"Running embedding with {len(inputs)} input(s)")

            embeddings = await loop.run_in_executor(
                self.executor,
                m.encode,
                inputs
            )
            
            logger.info(f"Successfully generated {len(embeddings)} embedding(s) using model '{model}'")
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings with model '{model}': {str(e)}", exc_info=True)
            raise