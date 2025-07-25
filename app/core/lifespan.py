from fastapi import FastAPI
from app.core.containers import Container
from contextlib import asynccontextmanager
from app.utils.logs import Logs

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    await container.init_resources()
    container.wire(modules=["app.routes"])
    app.container = container

    logs_repo = await container.logs_repo()
    Logs.init(logs_repo=logs_repo)

    yield
    await container.shutdown_resources()