from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorDetailResponse(BaseModel):
    field: str | None = None
    message: str


class ErrorBodyResponse(BaseModel):
    code: str
    message: str
    details: list[ErrorDetailResponse] | None = None
    trace_id: str | None = None


class ErrorResponse(BaseModel):
    error: ErrorBodyResponse


def build_error_response(
    *,
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
    trace_id: str | None = None,
) -> ErrorResponse:
    error_details = None
    if details is not None:
        error_details = [ErrorDetailResponse.model_validate(item) for item in details]
    return ErrorResponse(
        error=ErrorBodyResponse(
            code=code,
            message=message,
            details=error_details,
            trace_id=trace_id,
        )
    )
