from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
import os

from app.exceptions.PageAuthException import PageAuthException
from app.exceptions.SystemException import SystemException

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
    @app.exception_handler(PageAuthException)
    async def system_exception_handler(request: Request, exc: PageAuthException):
        requested_path = os.path.join("public", "401.html")
        return FileResponse(requested_path)

    @app.exception_handler(SystemException)
    async def system_exception_handler(request: Request, exc: SystemException):
        return JSONResponse(
            status_code=422,
            content={
                "code": exc.code,
                "message": exc.message,
                "data": {},
            },
        )