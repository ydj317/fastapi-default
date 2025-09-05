from fastapi import FastAPI
from app.core.containers import Container
from contextlib import asynccontextmanager
from app.core.settings import settings
from app.consumers.stream import stream_app

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    container.config.from_dict(settings.dict())

    await container.init_resources()

    container.wire(modules=["app.routes"])

    app.container = container

    # await stream_app.start()

    yield

    await container.shutdown_resources()

    # await stream_app.stop()
