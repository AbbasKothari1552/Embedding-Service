from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.core.provider_loader import load_providers
from app.core.model_registry import model_registry
from app.core.startup import preload_all_models
from app.logger.logging import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Embedding Service")

    try:
        # 1. Load providers
        logger.debug("Loading providers...")
        load_providers()
        logger.info("Providers loaded successfully")

        # 2. Load model registry
        logger.debug("Loading model registry from config/models.yaml...")
        model_registry.load_from_yaml("config/models.yaml")
        logger.info(f"Model registry loaded with {len(model_registry.models)} models")

        # 3. Preload all models
        logger.debug("Preloading all models...")
        await preload_all_models()
        logger.info("All models preloaded successfully")

        yield

    except Exception as e:
        logger.error(f"Startup error: {str(e)}", exc_info=True)
        raise

# Create FastAPI app with lifespan
app = FastAPI(
    title="Embedding Service Endpoint",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)