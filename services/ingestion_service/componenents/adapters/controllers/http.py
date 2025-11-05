from fastapi import APIRouter
from pydantic import BaseModel
from ..worker import enqueue_ingest

router = APIRouter()


class IngestRequest(BaseModel):
    url: str


class IngestResponse(BaseModel):
    video_id: str
    status: str


@router.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    video_id = enqueue_ingest(req.url)
    return IngestResponse(video_id=video_id, status="queued")
