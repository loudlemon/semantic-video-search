import shutil
import uuid
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Video Insight MVP (UV Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы с любого адреса (в т.ч. с localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage path (relative to container root)
UPLOAD_DIR = Path("../backend/data/videos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"file_id": file_id, "status": "uploaded"}


@app.get("/health")
async def health_check():
    """Returns 200 OK if the service is running"""
    return {"status": "ok", "service": "video-analyzer"}