from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_401_UNAUTHORIZED

from app.exceptions.PageAuthException import PageAuthException
from app.exceptions.SystemException import SystemException
from app.utils.error import error401, error500

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(Exception)
    async def catch_all_exceptions(request: Request, exc: Exception):
        accept_header = request.headers.get("accept", "").lower()
        if "text/html" in accept_header:
            return await error500(request)
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
        accept_header = request.headers.get("accept", "").lower()
        if "text/html" in accept_header:
            return await error401(request)
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={
                "code": HTTP_401_UNAUTHORIZED,
                "message": "Request validation error",
                "data": {},
            },
        )

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