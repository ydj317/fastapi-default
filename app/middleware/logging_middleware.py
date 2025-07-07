import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
import traceback

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("uvicorn.custom.access")

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception as exc:
            process_time = (time.perf_counter() - start_time) * 1000
            self.logger.error(
                f"❌ [ERROR] {request.method} {request.url.path} "
                f"→ {type(exc).__name__}: {exc} | {process_time:.2f} ms"
            )
            self.logger.debug(traceback.format_exc())
            raise

        process_time = (time.perf_counter() - start_time) * 1000
        self.logger.info(
            f"✅ {request.method} {request.url.path} "
            f"→ {response.status_code} | {process_time:.2f} ms"
        )
        return response
