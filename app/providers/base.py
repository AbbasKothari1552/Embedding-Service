# providers/base.py

from abc import ABC, abstractmethod
from typing import List
from app.logger.logging import get_logger

logger = get_logger(__name__)

class EmbeddingProvider(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def embed(self, model: str, inputs: List[str]) -> List[List[float]]:
        pass