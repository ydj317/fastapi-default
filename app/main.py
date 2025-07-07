from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.containers import Container
from contextlib import asynccontextmanager
from app.routes import router
from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    app.container = container
    await container.init_resources()
    yield
    await container.shutdown_resources()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Server Error", "detail": str(exc)},
    )

app.add_middleware(LoggingMiddleware)

app.include_router(router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
