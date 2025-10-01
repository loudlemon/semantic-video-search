from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from services.indexing_service.application.app import app
from services.indexing_service.application.endpoints import router


# Configure CORS to allow your React app (running on default ports/hosts) to communicate
origins = [
    "http://localhost",
    "http://localhost:3000",  # Default React development server port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Simulation Data Stores ---
uploaded_video_path = None
uploaded_image_path = None


app.include_router(router, prefix="/api/v1", tags=["Semantic Video Search"])


if __name__ == "__main__":
    # To run the server: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)