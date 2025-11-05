from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    FieldCondition,
    Filter,
    MatchValue,
    NamedVector,
)

from ...domain.entities import FrameMatch
from ...domain.repositories import VectorIndexRepository


class QdrantVectorRepository(VectorIndexRepository):

    def __init__(self, client: QdrantClient, collection_name: str):
        self._client = client
        self._collection = collection_name

    async def search_by_embedding(
        self,
        vector: list[float],
        top_k: int,
        video_id: Optional[str] = None
    ) -> List[FrameMatch]:
        cond = None
        if video_id:
            cond = Filter(
                must=[
                    FieldCondition(
                        key="video_id", match=MatchValue(value=video_id)
                    )
                ]
            )

        res = self._client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=top_k,
            query_filter=cond,
            with_payload=True,
            with_vectors=False,
        )
        matches: List[FrameMatch] = []
        for p in res:
            payload = p.payload or {}
            matches.append(
                FrameMatch(
                    video_id=payload.get("video_id", ""),
                    timestamp_sec=float(payload.get("timestamp_sec", 0.0)),
                    caption=payload.get("caption"),
                    thumbnail_url=payload.get("thumbnail_url"),
                    score=float(p.score),
                )
            )
        return matches
