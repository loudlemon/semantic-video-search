import os
from dataclasses import dataclass


@dataclass
class Settings:
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8080"))

    embedding_base_url: str = os.getenv(
        "EMBEDDING_BASE_URL", "http://embedding-service:8000"
    )
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_api_key: str | None = os.getenv("QDRANT_API_KEY")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "frames")

    postgres_dsn: str = os.getenv(
        "POSTGRES_DSN",
        "postgresql://postgres:postgres@postgres:5432/semvid",
    )
