from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from app.routes import router
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utils.template import Template
import os

def register_routers(app: FastAPI):
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="template/static"), name="static")
    app.mount("/uploads", StaticFiles(directory="uploads"), name="static")

    @app.get("/")
    async def main_page(template: Template = Depends()):
        return await template.response('index.html')

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            requested_public_path = os.path.join("public", request.url.path.lstrip("/"))
            if os.path.isfile(requested_public_path):
                return FileResponse(requested_public_path)
            requested_template_path = os.path.join("template", request.url.path.lstrip("/"))
            if os.path.isfile(requested_template_path):
                return await Template(request).response(request.url.path.lstrip("/"))

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": {},
            },
        )