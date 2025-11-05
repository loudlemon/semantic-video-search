from dataclasses import dataclass
from typing import Optional, List


@dataclass(frozen=True)
class FrameMatch:
    video_id: str
    timestamp_sec: float
    caption: Optional[str]
    thumbnail_url: Optional[str]
    score: float  # similarity score (the higher the better)


@dataclass(frozen=True)
class SearchQuery:
    text: str
    video_id: Optional[str] = None
    top_k: int = 10
