import asyncio
import signal
from fastapi import FastAPI
import uvicorn


from ..adapters.controllers.http import router
from ..adapters import di
from ..application.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title="Semantic Video Search Service", version="0.1.0")
    @app.on_event("startup")
    async def on_startup():
        di.container = di.Container(settings)

    @app.on_event("shutdown")
    async def on_shutdown():
        if di.container:
            await di.container.aclose()

    app.include_router(router, prefix="/v1")
    return app


if __name__ == "__main__":
    settings = Settings()
    app = create_app(settings)
    uvicorn.run(app, host=settings.host, port=settings.port)
