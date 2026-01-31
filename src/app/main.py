from fastapi import FastAPI

from .api.routers import (
    healthz_router, 
    antifraud_router, 
    metrics_router)
from app.metrics.http import PrometheusMiddleware

def create_app() -> FastAPI:
    app = FastAPI(title="Антифрод сервис")

    app.add_middleware(PrometheusMiddleware)

    app.include_router(healthz_router)
    app.include_router(antifraud_router)
    app.include_router(metrics_router)

    return app

app = create_app()