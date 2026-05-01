from __future__ import annotations

from typing import Any
from uuid import UUID

from pydantic import BaseModel


class TaskAuditBase(BaseModel):
    task_id: UUID
    action: str
    before_state: dict[str, Any] | None = None
    after_state: dict[str, Any] | None = None
