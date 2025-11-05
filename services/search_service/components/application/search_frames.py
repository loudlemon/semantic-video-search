from typing import List

from ..domain.entities import FrameMatch, SearchQuery
from ..domain.repositories import (
    EmbeddingProvider,
    MetadataRepository,
    VectorIndexRepository,
)


class SearchFramesUseCase:

    def __init__(
        self,
        embedder: EmbeddingProvider,
        vector_repo: VectorIndexRepository,
        metadata_repo: MetadataRepository,
    ):
        self._embedder = embedder
        self._vector_repo = vector_repo
        self._metadata_repo = metadata_repo

    async def execute(self, query: SearchQuery) -> List[FrameMatch]:
        if query.video_id is not None:
            exists = await self._metadata_repo.video_exists(query.video_id)
            if not exists:
                # For alpha we don't raise; we return empty.
                return []

        vector = await self._embedder.embed_text(query.text)
        matches = await self._vector_repo.search_by_embedding(
            vector=vector, top_k=query.top_k, video_id=query.video_id
        )
        return matches
