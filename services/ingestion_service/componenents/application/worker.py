import os
from celery import Celery
from qdrant_client import QdrantClient
from .config import Settings
from ..infrastructure.video.downloader import SimpleDownloader
from ..infrastructure.video.ffmpeg_extractor import FFmpegExtractor
from ..infrastructure.caption.http_captioner import HttpCaptioner
from ..infrastructure.embed.http_embedder import HttpEmbedder
from ..infrastructure.storage.minio_storage import MinioStorage
from ..infrastructure.vector.qdrant_repo import QdrantVectorRepository
from ..infrastructure.db.postgres_metadata_repo import PostgresMetadata
from ..application.ingest_video import IngestVideoUseCase

settings = Settings()
celery_app = Celery("ingestion", broker=settings.redis_url, backend=settings.redis_url)

_downloader = SimpleDownloader()
_extractor = FFmpegExtractor()
_captioner = HttpCaptioner(settings.caption_base_url)
_embedder = HttpEmbedder(settings.embedding_base_url)
_storage = MinioStorage(settings.minio_endpoint, settings.minio_access_key, settings.minio_secret_key, settings.minio_bucket, settings.minio_secure)
_qdrant = QdrantClient(url=settings.qdrant_url, timeout=30)
_vector_repo = QdrantVectorRepository(_qdrant, settings.qdrant_collection)
_metadata = PostgresMetadata(settings.postgres_dsn)

_uc = IngestVideoUseCase(
    downloader=_downloader,
    extractor=_extractor,
    captioner=_captioner,
    embedder=_embedder,
    storage=_storage,
    vector_repo=_vector_repo,
    metadata=_metadata,
    fps=1,
)

@celery_app.task
def ingest_task(source_url: str) -> str:
    return _uc.execute(source_url)


def enqueue_ingest(source_url: str) -> str:
    vid = _metadata.create_video(source_url)
    celery_app.send_task("ingestion_service.worker.ingest_task", args=[source_url])
    # set to queued now; worker will update to processing/ready
    _metadata.set_status(vid, "queued")
    return vid
