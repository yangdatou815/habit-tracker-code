from __future__ import annotations

import time
import uuid

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        structlog.contextvars.clear_contextvars()

        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "request.completed",
                status_code=response.status_code,
                duration_ms=round(duration_ms, 2),
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.exception("request.failed", duration_ms=round(duration_ms, 2))
            raise
