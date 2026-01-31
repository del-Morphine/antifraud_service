import time
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
from fastapi import Request

REQUEST_COUNT = Counter(
    "http_request_total",
    "Total number of HTTP requests",
    ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "path", "status"]
)

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status=response.status_code,
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
            status=response.status_code,
        ).observe(duration)

        return response