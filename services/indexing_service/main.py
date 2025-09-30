from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
import json
import uuid
import asyncio
from typing import List, Dict, Any
from services.user_ui.page import get_frontend_html
from mocks import (
    MockEmbedder, MockVideoProcessor, MockDatabase, MockTaskTracker, 
    MOCK_DB, TASK_STATUSES
)
from models import EtalonData, SearchResult, TaskStatus

app = FastAPI(title="Video Search Backend")

# --- Global Component Initialization ---
embedder = MockEmbedder()
video_processor = MockVideoProcessor(total_frames=50) # Mock video has 50 frames
db = MockDatabase()
task_tracker = MockTaskTracker()

# --- Helper Functions ---

def calculate_cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculates the cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_a = (sum(a * a for a in vec1)) ** 0.5
    norm_b = (sum(b * b for b in vec2)) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# --- Core Processing Logic (Indexing and Searching) ---


async def index_video_job(video_path: str, etalon_id: str, similarity_threshold: float):
    task_id = task_tracker.create_task(f"Indexing video: {video_path}")
    
    try:
        await task_tracker.update_status(task_id, "EXTRACTING_FRAMES", 5, "Extracting frames from video...")
        frame_indices = await video_processor.extract_frames(video_path)
        total_frames = len(frame_indices)
        
        # Retrieve required etalon data
        etalon_data = await db.get_etalon(etalon_id)
        if not etalon_data:
            raise ValueError(f"Etalon ID {etalon_id} not found.")

        # 1. Indexing Phase
        for i, frame_index in enumerate(frame_indices):
            progress = int(30 + (i / total_frames) * 40) # Progress from 30% to 70%
            
            await task_tracker.update_status(task_id, "INDEXING_FRAMES", progress, f"Processing frame {frame_index}/{total_frames}")

            # Mock: Assume we get an image embed and generate a placeholder text embed for the frame
            frame_image_embed = embedder.generate(f"{video_path}_frame_{frame_index}")
            
            # IMPORTANT: For indexing, we use the *etalon text* embed combined with the frame image embed.
            # In a more complex setup, the frame itself might have a caption generated here.
            frame_text_embed = etalon_data['text_embed'] 
            
            frame_data = {
                "video_id": video_path.split('/')[-1], # Use filename as mock video ID
                "frame_index": frame_index,
                "image_embed": frame_image_embed,
                "text_embed": frame_text_embed,
                "text_description": f"Frame {frame_index} description placeholder"
            }
            await db.save_frame(frame_data)
            await asyncio.sleep(0.01) # Simulate I/O wait

        # 2. Search Phase (Comparing all frames against the Etalon)
        await task_tracker.update_status(task_id, "SEARCHING", 75, "Calculating similarity scores...")
        
        search_results: List[SearchResult] = []
        all_frames = await db.get_all_frames()
        
        for frame in all_frames:
            # Combine Image and Text similarity (Simple average for this mock)
            img_sim = calculate_cosine_similarity(frame['image_embed'], etalon_data['image_embed'])
            txt_sim = calculate_cosine_similarity(frame['text_embed'], etalon_data['text_embed'])
            
            # Simple combined score: Average the two similarities
            combined_score = (img_sim + txt_sim) / 2
            
            if combined_score >= similarity_threshold:
                search_results.append(SearchResult(
                    frame_id=f"{frame['video_id']}_{frame['frame_index']}",
                    video_id=frame['video_id'],
                    frame_index=frame['frame_index'],
                    similarity_score=combined_score
                ))
            await asyncio.sleep(0.005) # Simulate search calculation

        # Sort results by score descending
        search_results.sort(key=lambda x: x['similarity_score'], reverse=True)

        # 3. Finalize
        final_message = f"Search complete. Found {len(search_results)} matching segments."
        await task_tracker.update_status(task_id, "COMPLETE", 100, final_message)
        
        # Store results attached to the task (or a separate result table)
        TASK_STATUSES[task_id]["result"] = search_results
        
    except Exception as e:
        print(f"Job failed: {e}")
        await task_tracker.update_status(task_id, "FAILED", 100, f"Processing failed: {str(e)}")


# --- API Endpoints ---

@app.get("/")
async def get_index_html():
    # Serve the simple HTML/JS client for testing
    return HTMLResponse(content=get_frontend_html(), media_type="text/html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket Client Connected.")
    
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            payload = data.get("payload", {})
            
            if action == "GET_STATUS":
                task_id = payload.get("task_id")
                status = task_tracker.get_status(task_id)
                await websocket.send_json({"type": "STATUS_UPDATE", "data": status})

            elif action == "START_INDEXING":
                video_path = payload.get("video_path", "/mock/video1.mp4")
                etalon_filename = payload.get("etalon_filename", "etalon_car_1.jpg")
                threshold = float(payload.get("threshold", 0.85))
                
                # --- Mock Etalon Setup ---
                # Since we don't upload files, we mock the etalon creation here
                etalon_id = f"ETALON-{uuid.uuid4().hex[:6]}"
                await db.save_etalon(
                    etalon_id=etalon_id,
                    image_embed=embedder.generate(f"Image of {etalon_filename}"),
                    text_embed=embedder.generate("The text description for the etalon.")
                )
                
                # Start the long-running job in the background
                asyncio.create_task(
                    index_video_job(video_path, etalon_id, threshold)
                )
                
                # Immediately send back the task ID so the client can poll/listen
                await websocket.send_json({"type": "TASK_STARTED", "task_id": task_tracker.create_task("Initializing...")})
                
            else:
                await websocket.send_json({"type": "ERROR", "message": "Unknown action"})

    except WebSocketDisconnect:
        print("WebSocket Client Disconnected.")
    except Exception as e:
        print(f"WebSocket Error: {e}")

# --- Background Status Broadcaster ---
# This task periodically broadcasts the status of all active tasks to all connected clients.

@app.on_event("startup")
async def startup_event():
    # Start the background task runner
    asyncio.create_task(status_broadcaster())

async def status_broadcaster():
    active_connections: List[WebSocket] = []
    
    while True:
        # 1. Update connections list (FastAPI doesn't expose active sockets easily, 
        # so this part is highly simplified for a monolithic example)
        # In a production app, you'd manage active_connections explicitly in the websocket_endpoint.
        
        # For this simple mock, we just check the global status dictionary
        statuses_to_send = [s for s in TASK_STATUSES.values() if s['progress'] < 100]
        
        if statuses_to_send:
            # NOTE: Since we don't have a centralized connection manager, 
            # we can only send this data if we refresh the frontend or if the client polls.
            # For this demo, we assume the client polls via GET_STATUS, 
            # but we keep this loop to show the intent.
            print(f"Broadcasting {len(statuses_to_send)} active statuses...")
            # In a real setup:
            # for conn in active_connections:
            #     await conn.send_json({"type": "STATUS_UPDATE", "data": statuses_to_send})
        
        await asyncio.sleep(2) # Check every 2 seconds

