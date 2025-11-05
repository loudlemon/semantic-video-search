from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import FrameMatch


class EmbeddingProvider(ABC):

    @abstractmethod
    async def embed_text(self, text: str) -> list[float]:
        ...


class VectorIndexRepository(ABC):

    @abstractmethod
    async def search_by_embedding(
        self,
        vector: list[float],
        top_k: int,
        video_id: Optional[str] = None
    ) -> List[FrameMatch]:
        ...


class MetadataRepository(ABC):

    @abstractmethod
    async def resolve_video_id(self, source_url: str) -> Optional[str]:
        ...

    @abstractmethod
    async def video_exists(self, video_id: str) -> bool:
        ...
