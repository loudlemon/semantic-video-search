from typing import TypedDict, List, Dict, Any

# --- Mock Database Structures ---


class EtalonData(TypedDict):
    etalon_id: str
    image_embed: List[float]
    text_embed: List[float]


class FrameData(TypedDict):
    frame_index: int
    image_embed: List[float]
    text_description: str # Original text used to generate the text embed (for debugging)
    text_embed: List[float]
    video_id: str


class VectorDatabase(TypedDict):
    # Stores indexed frames
    frames: Dict[str, FrameData] # Key: Unique Frame ID (e.g., video_id_frame_index)
    etalons: Dict[str, EtalonData] # Key: Etalon ID

# --- Task Management ---


class TaskStatus(TypedDict):
    task_id: str
    status: str # e.g., 'PENDING', 'INDEXING_FRAMES', 'SEARCHING', 'COMPLETE', 'FAILED'
    progress: int # Percentage 0-100
    message: str
    result: Any | None

# --- Search Results ---


class SearchResult(TypedDict):
    frame_id: str
    video_id: str
    frame_index: int
    similarity_score: float
    # Note: We need a way to map frame_id back to a short video clip later. 
    # For now, we return the index.
