from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import os

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def catch_all_exceptions(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": f"Server Error",
                "data": {"detail": str(exc)},
            },
        )

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

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail,
                "data": {},
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "code": HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Request validation error",
                "data": {"errors": exc.errors()},
            },
        )