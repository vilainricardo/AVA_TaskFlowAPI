from fastapi import FastAPI

import app.models  # noqa: F401

from app.core.config import Settings, get_settings
from app.core.database import ping_database

settings: Settings = get_settings()

app: FastAPI = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    db_status = "up" if ping_database() else "down"
    return {
        "status": "ok",
        "database": db_status,
        "environment": settings.environment,
    }
