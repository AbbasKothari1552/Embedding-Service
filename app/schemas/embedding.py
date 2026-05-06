from pydantic import BaseModel, Field
from typing import List, Union
from app.logger.logging import get_logger

logger = get_logger(__name__)

class EmbeddingRequest(BaseModel):
    provider: str = Field(..., example="local")
    model: str = Field(..., example="all-MiniLM-L6-v2")
    input: Union[str, List[str]]

class EmbeddingResponse(BaseModel):
    model: str
    embeddings: List[List[float]]