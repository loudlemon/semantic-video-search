import os
import uuid
from ..domain.interfaces import (
    VideoDownloader, FrameExtractor, Captioner, Embedder,
    ObjectStorage, VectorIndexRepository, MetadataRepository
)


class IngestVideoUseCase:
    def __init__(
        self,
        downloader: VideoDownloader,
        extractor: FrameExtractor,
        captioner: Captioner,
        embedder: Embedder,
        storage: ObjectStorage,
        vector_repo: VectorIndexRepository,
        metadata: MetadataRepository,
        fps: int = 1,
    ):
        self._downloader = downloader
        self._extractor = extractor
        self._captioner = captioner
        self._embedder = embedder
        self._storage = storage
        self._vector = vector_repo
        self._meta = metadata
        self._fps = fps

    def execute(self, source_url: str) -> str:
        video_id = self._meta.create_video(source_url)
        self._meta.set_status(video_id, "processing")

        video_path = self._downloader.download(source_url)
        try:
            for ts, frame_path in self._extractor.extract(video_path, fps=self._fps):
                caption = self._captioner.caption(frame_path)
                vec = self._embedder.embed_text(caption)
                object_key = f"frames/{video_id}/{int(ts*1000)}.jpg"
                thumb_url = self._storage.upload(frame_path, object_key)
                self._vector.upsert_frame(
                    vector=vec,
                    video_id=video_id,
                    timestamp_sec=ts,
                    caption=caption,
                    thumbnail_url=thumb_url,
                )
        finally:
            if os.path.exists(video_path):
                try:
                    os.remove(video_path)
                except Exception:
                    pass

        self._meta.set_status(video_id, "ready")
        return video_id
