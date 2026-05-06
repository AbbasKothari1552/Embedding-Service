from fastapi import APIRouter, HTTPException
from app.schemas.embedding import EmbeddingRequest, EmbeddingResponse
from app.engine.embedding_engine import EmbeddingEngine
from app.logger.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()
engine = EmbeddingEngine()


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