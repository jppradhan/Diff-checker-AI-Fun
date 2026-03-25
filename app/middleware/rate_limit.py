from collections import defaultdict, deque
from time import monotonic
from typing import Deque, Dict, Tuple
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory per-IP and per-path fixed-window rate limiting."""

    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.window_seconds = 60
        self.default_limit = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "120"))
        self.path_limits = {
            "/check_diff_agent": int(os.getenv("API_RATE_LIMIT_CHECK_DIFF_PER_MINUTE", "20")),
            "/health": int(os.getenv("API_RATE_LIMIT_HEALTH_PER_MINUTE", "600")),
            "/tools": int(os.getenv("API_RATE_LIMIT_TOOLS_PER_MINUTE", "120")),
            "/": int(os.getenv("API_RATE_LIMIT_ROOT_PER_MINUTE", "120")),
        }
        self._requests: Dict[Tuple[str, str], Deque[float]] = defaultdict(deque)

    def _limit_for_path(self, path: str) -> int:
        return self.path_limits.get(path, self.default_limit)

    async def dispatch(self, request: Request, call_next):
        limit = self._limit_for_path(request.url.path)
        if limit <= 0:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        bucket_key = (client_ip, request.url.path)
        now = monotonic()
        bucket = self._requests[bucket_key]

        while bucket and (now - bucket[0]) >= self.window_seconds:
            bucket.popleft()

        if len(bucket) >= limit:
            retry_after = max(1, int(self.window_seconds - (now - bucket[0])))
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "path": request.url.path,
                    "limit_per_minute": limit,
                    "retry_after_seconds": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )

        bucket.append(now)
        return await call_next(request)
