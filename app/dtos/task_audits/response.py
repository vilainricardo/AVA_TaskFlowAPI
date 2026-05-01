from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.dtos.task_audits.base import TaskAuditBase


class TaskAuditReadResponse(TaskAuditBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
