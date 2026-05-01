from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.dtos.tasks.base import TaskBase


class TaskReadResponse(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
