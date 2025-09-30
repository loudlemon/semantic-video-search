import random
import time
import asyncio
from typing import List, Dict, Any
from models import VectorDatabase, TaskStatus, EtalonData, SearchResult

# --- Mock Data Storage ---
MOCK_DB: VectorDatabase = {
    "frames": {},
    "etalons": {}
}
TASK_STATUSES: Dict[str, TaskStatus] = {}

# --- Mock Services ---

class MockEmbedder:
    """Simulates CLIP model generating embeddings."""
    def generate(self, input_data: str) -> List[float]:
        # Generates a fixed-size mock embedding vector
        # In a real scenario, this would be a call to a model (e.g., CLIP)
        return [random.uniform(-1.0, 1.0) for _ in range(128)]

class MockVideoProcessor:
    """Simulates video frame extraction."""
    def __init__(self, total_frames: int = 50):
        self.total_frames = total_frames

    async def extract_frames(self, video_path: str) -> List[int]:
        print(f"Mock: Processing video at {video_path}...")
        await asyncio.sleep(1) # Simulate initial setup delay
        return list(range(self.total_frames))

class MockDatabase:
    """Simulates Vector DB operations."""
    
    async def save_etalon(self, etalon_id: str, image_embed: List[float], text_embed: List[float]):
        MOCK_DB["etalons"][etalon_id] = {
            "etalon_id": etalon_id,
            "image_embed": image_embed,
            "text_embed": text_embed
        }
        print(f"Mock DB: Saved Etalon {etalon_id}")

    async def save_frame(self, frame_data: Dict[str, Any]):
        frame_id = f"{frame_data['video_id']}_{frame_data['frame_index']}"
        MOCK_DB["frames"][frame_id] = FrameData(
            frame_index=frame_data['frame_index'],
            image_embed=frame_data['image_embed'],
            text_description=frame_data['text_description'],
            text_embed=frame_data['text_embed'],
            video_id=frame_data['video_id']
        )
        # print(f"Mock DB: Saved Frame {frame_id}")

    async def get_etalon(self, etalon_id: str) -> EtalonData | None:
        return MOCK_DB["etalons"].get(etalon_id)

    async def get_all_frames(self) -> List[FrameData]:
        return list(MOCK_DB["frames"].values())

# --- Task Management ---


class MockTaskTracker:
    """Manages task status updates."""
    
    def __init__(self):
        self.task_id_counter = 1000

    def create_task(self, message: str) -> str:
        task_id = f"TASK-{self.task_id_counter}"
        self.task_id_counter += 1
        TASK_STATUSES[task_id] = TaskStatus(
            task_id=task_id,
            status="PENDING",
            progress=0,
            message=message,
            result=None
        )
        return task_id

    async def update_status(self, task_id: str, status: str, progress: int, message: str):
        if task_id in TASK_STATUSES:
            TASK_STATUSES[task_id]["status"] = status
            TASK_STATUSES[task_id]["progress"] = min(100, max(0, progress)) # Clamp 0-100
            TASK_STATUSES[task_id]["message"] = message
            # In a real app, this would trigger a WebSocket broadcast
            await asyncio.sleep(0.01) # Simulate non-blocking update

    def get_status(self, task_id: str) -> TaskStatus | None:
        return TASK_STATUSES.get(task_id)
