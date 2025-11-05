import os
from dataclasses import dataclass


@dataclass
class Settings:
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8001"))

    embedding_base_url: str = os.getenv("EMBEDDING_BASE_URL", "http://embedding-service:8000")
    caption_base_url: str = os.getenv("CAPTION_BASE_URL", "http://captioning-service:8002")

    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "frames")

    minio_endpoint: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "thumbnails")
    minio_secure: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"

    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    postgres_dsn: str = os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@postgres:5432/semvid")
