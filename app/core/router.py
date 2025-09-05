from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from app.routes import router
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.template import Template
from pathlib import Path
from app.utils.error import error404
import os

def register_routers(app: FastAPI):
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="static")

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            response = await handle_404(request)
            if response:
                return response

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": {},
            },
        )

async def handle_404(request: Request):
    url_path = request.url.path.lstrip("/")
    accept_header = request.headers.get("accept", "").lower()

    public_path = Path("public") / url_path
    if public_path.is_file():
        return FileResponse(public_path)

    template_path = Path("template") / f"{url_path}.j2"
    if "text/html" in accept_header:
        if template_path.is_file():
            return await Template(request).response(f"{url_path}.j2")
        return await error404(request)

    return None