from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskAuditBase(BaseModel):
    task_id: UUID
    action: str
    before_state: dict[str, Any] | None = None
    after_state: dict[str, Any] | None = None


class TaskAuditCreate(TaskAuditBase):
    pass


class TaskAuditRead(TaskAuditBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
