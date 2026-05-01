from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

import app.models  # noqa: F401

from app.core.config import Settings, get_settings
from app.core.database import ping_database
from app.core.exceptions import ApiException
from app.dtos.errors import build_error_response
from app.routers import tasks_router

settings: Settings = get_settings()

app: FastAPI = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)

app.include_router(tasks_router, prefix=settings.api_v1_prefix)


@app.exception_handler(ApiException)
def handle_api_exception(_: Request, exc: ApiException) -> JSONResponse:
    trace_id: str = str(uuid4())
    response = build_error_response(
        code=exc.code,
        message=exc.message,
        details=exc.details,
        trace_id=trace_id,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )


@app.exception_handler(RequestValidationError)
def handle_validation_exception(_: Request, exc: RequestValidationError) -> JSONResponse:
    trace_id: str = str(uuid4())
    details = []
    for error in exc.errors():
        loc = error.get("loc", [])
        details.append(
            {
                "field": str(loc[-1]) if len(loc) > 0 else None,
                "message": error.get("msg", "Invalid value."),
            }
        )
    response = build_error_response(
        code="VALIDATION_ERROR",
        message="Request payload validation failed.",
        details=details,
        trace_id=trace_id,
    )
    return JSONResponse(status_code=422, content=response.model_dump(mode="json"))


@app.exception_handler(SQLAlchemyError)
def handle_database_exception(_: Request, __: SQLAlchemyError) -> JSONResponse:
    trace_id: str = str(uuid4())
    response = build_error_response(
        code="DATABASE_ERROR",
        message="Database operation failed.",
        trace_id=trace_id,
    )
    return JSONResponse(status_code=503, content=response.model_dump(mode="json"))


@app.exception_handler(Exception)
def handle_unexpected_exception(_: Request, __: Exception) -> JSONResponse:
    trace_id: str = str(uuid4())
    response = build_error_response(
        code="INTERNAL_SERVER_ERROR",
        message="Unexpected internal error.",
        trace_id=trace_id,
    )
    return JSONResponse(status_code=500, content=response.model_dump(mode="json"))


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    db_status = "up" if ping_database() else "down"
    return {
        "status": "ok",
        "database": db_status,
        "environment": settings.environment,
    }
