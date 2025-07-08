from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.containers import Container
from contextlib import asynccontextmanager
from app.routes import router
from app.core.logging_config import setup_logging
from app.db.database import database
from app.middleware.logging_middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
import os

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    await container.init_resources()
    container.wire(modules=["app.routes"])

    app.container = container

    await database.connect()
    print("✅ Database connected")

    yield

    await database.disconnect()
    print("🔌 Database disconnected")

    await container.shutdown_resources()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def catch_all_exceptions(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Server Error", "detail": str(exc)},
    )

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

# ✅ 없는 라우트 fallback: public/index.html 또는 404.html 등
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # 요청 경로에 맞는 파일이 public에 있으면 해당 파일 서빙
        requested_path = os.path.join("public", request.url.path.lstrip("/"))
        if os.path.isfile(requested_path):
            return FileResponse(requested_path)
        else:
            index_path = os.path.join("public", "index.html")
            if os.path.isfile(index_path):
                return FileResponse(index_path)
    # 기본 예외 핸들링
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )