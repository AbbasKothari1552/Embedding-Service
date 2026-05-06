from fastapi import APIRouter, HTTPException
from app.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from app.engine.embedding_engine import EmbeddingEngine
from app.core.provider_loader import PROVIDERS
from app.core.model_registry import model_registry
from app.logger.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()
engine = EmbeddingEngine()


@router.get("/health")
async def health_check():
    provider_count = len(PROVIDERS)
    model_count = len(model_registry.models)
    provider_statuses = []

    for name, provider in PROVIDERS.items():
        loaded_models = getattr(provider, "models", None)
        provider_statuses.append({
            "name": name,
            "loaded_models": len(loaded_models) if isinstance(loaded_models, dict) else None,
        })

    if provider_count == 0:
        raise HTTPException(status_code=503, detail="No providers loaded")

    if model_count == 0:
        raise HTTPException(status_code=503, detail="No models loaded")

    return {
        "status": "ok",
        "provider_count": provider_count,
        "model_count": model_count,
        "providers": provider_statuses,
    }


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embedding(req: EmbeddingRequest):
    logger.debug(f"Embedding request received - provider: {req.provider}, model: {req.model}")

    try:
        result = await engine.embed(
            provider=req.provider,
            model=req.model,
            input_data=req.input
        )
        logger.info(f"Successfully generated embeddings for model: {req.model}")

        return EmbeddingResponse(
            model=req.model,
            embeddings=result
        )

    except ValueError as e:
        logger.error(f"Validation error in embedding request: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in embedding request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    logger.debug("Fetching list of available models")
    from app.core.model_registry import model_registry
    models = model_registry.list_models()
    logger.info(f"Returning {len(models)} available models")
    return {"models": models}