from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid


class QdrantVectorRepository:
    def __init__(self, client: QdrantClient, collection: str):
        self._client = client
        self._collection = collection

    def upsert_frame(self, vector, video_id, timestamp_sec, caption, thumbnail_url):
        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "video_id": video_id,
                "timestamp_sec": timestamp_sec,
                "caption": caption,
                "thumbnail_url": thumbnail_url,
            },
        )
        self._client.upsert(collection_name=self._collection, points=[point])
