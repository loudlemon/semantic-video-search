import httpx
from qdrant_client import QdrantClient

from ..application.config import Settings
from ..application.search_frames import SearchFramesUseCase
from ..infrastructure.db.postgres_metadata_repo import (
    PostgresMetadataRepository,
)
from ..infrastructure.embedding.http_embed_provider import HttpEmbeddingProvider
from ..infrastructure.vector.qdrant_repo import QdrantVectorRepository


class Container:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.http_client = httpx.AsyncClient(timeout=20.0, base_url="")
        self.embedder = HttpEmbeddingProvider(
            base_url=settings.embedding_base_url, client=self.http_client
        )
        self.qdrant = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key or None,
            timeout=20,
        )
        self.vector_repo = QdrantVectorRepository(
            client=self.qdrant,
            collection_name=settings.qdrant_collection,
        )
        self.metadata_repo = PostgresMetadataRepository(
            dsn=settings.postgres_dsn
        )
        self.search_use_case = SearchFramesUseCase(
            embedder=self.embedder,
            vector_repo=self.vector_repo,
            metadata_repo=self.metadata_repo,
        )

    async def aclose(self):
        await self.http_client.aclose()


container: Container | None = None
