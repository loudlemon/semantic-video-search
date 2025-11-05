from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ...application.search_frames import SearchFramesUseCase
from ...domain.entities import FrameMatch, SearchQuery


class FrameMatchDTO(BaseModel):
    video_id: str
    timestamp_sec: float
    caption: Optional[str] = None
    thumbnail_url: Optional[str] = None
    score: float


class SearchRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)
    video_id: Optional[str] = None
    top_k: int = 10


router = APIRouter()


def get_use_case() -> SearchFramesUseCase:
    # Wired in main via DI container; replaced in tests.
    from ..di import container
    return container.search_use_case


@router.post("/search", response_model=List[FrameMatchDTO])
async def search_endpoint(
    req: SearchRequest, uc: SearchFramesUseCase = Depends(get_use_case)
):
    query = SearchQuery(text=req.text, video_id=req.video_id, top_k=req.top_k)
    results: List[FrameMatch] = await uc.execute(query)
    return [FrameMatchDTO(**vars(m)) for m in results]
