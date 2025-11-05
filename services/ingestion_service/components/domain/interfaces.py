from abc import ABC, abstractmethod
from typing import Iterable, Optional


class VideoDownloader(ABC):

    @abstractmethod
    def download(self, url: str) -> str:
        """Returns local file path."""
        ...


class FrameExtractor(ABC):

    @abstractmethod
    def extract(self, video_path: str, fps: int) -> Iterable[tuple[float, str]]:
        """Yields (timestamp_sec, frame_image_path)."""
        ...


class Captioner(ABC):

    @abstractmethod
    def caption(self, image_path: str) -> str:
        ...


class Embedder(ABC):

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        ...


class ObjectStorage(ABC):

    @abstractmethod
    def upload(self, local_path: str, object_key: str) -> str:
        """Returns public URL (or presigned)."""
        ...


class VectorIndexRepository(ABC):

    @abstractmethod
    def upsert_frame(
        self,
        vector: list[float],
        video_id: str,
        timestamp_sec: float,
        caption: str,
        thumbnail_url: str,
    ) -> None:
        ...


class MetadataRepository(ABC):

    @abstractmethod
    def create_video(self, source_url: str) -> str:
        ...

    @abstractmethod
    def set_status(self, video_id: str, status: str) -> None:
        ...
