import uvicorn
from fastapi import FastAPI

from ..adapters.controllers.http import router
from ..application.config import Settings

app = FastAPI(title="Ingestion Service", version="0.1.0")
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(app, host=settings.host, port=settings.port)
