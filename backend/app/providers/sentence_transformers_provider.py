"""
SentenceTransformers Concrete Embedding Provider Implementation.
"""

from typing import List, Optional
from sentence_transformers import SentenceTransformer
from app.core.config import settings
from app.core.interfaces.embedding_provider import IEmbeddingProvider
from app.core.logging import logger


class SentenceTransformerEmbeddingProvider(IEmbeddingProvider):
    """Concrete implementation of IEmbeddingProvider wrapping sentence-transformers."""

    def __init__(self, model_name: Optional[str] = None):
        self._model_name = model_name or settings.EMBEDDING_MODEL_NAME
        self._model: Optional[SentenceTransformer] = None

    def _get_model(self) -> SentenceTransformer:
        """Lazy-loads the SentenceTransformer model."""
        if self._model is None:
            logger.info(f"Loading SentenceTransformer model '{self._model_name}'")
            self._model = SentenceTransformer(self._model_name)
        return self._model

    def encode(self, texts: List[str]) -> List[List[float]]:
        """Encodes a list of texts into vector embeddings."""
        if not texts:
            return []
        model = self._get_model()
        return model.encode(texts).tolist()
