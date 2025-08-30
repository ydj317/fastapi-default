from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.context import set_trace_id, set_is_login, set_username
from app.core.auth import get_token_by_cookie_no_except

def register_middleware(app: FastAPI):
    app.add_middleware(TraceIDMiddleware)
    app.add_middleware(CheckLoginMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

class TraceIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        set_trace_id(trace_id)
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response

class CheckLoginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = await get_token_by_cookie_no_except(request)
        set_username(token.sub)
        set_is_login(token.sub is not '')
        request.state.username = token.sub
        request.state.is_login = token.sub is not ''
        response = await call_next(request)
        return response

