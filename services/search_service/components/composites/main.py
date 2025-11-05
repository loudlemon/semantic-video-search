import asyncio
import signal
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from ..adapters import di
from ..adapters.controllers.https import router
from ..application.config import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup: Loading...")
    di.container = di.Container(settings)
    yield    # Application can now accept requests

    # Shutdown events: Clean up resources
    print("Application shutdown: Unloading...")
    if di.container:
        await di.container.aclose()


def create_app(lifespan) -> FastAPI:
    app = FastAPI(
        title="Semantic Video Search Service",
        version="0.1.0",
        lifespan=lifespan
    )

    app.include_router(router, prefix="/v1")
    return app


if __name__ == "__main__":
    settings = Settings()
    app = create_app(lifespan)
    uvicorn.run(app, host=settings.host, port=settings.port)
