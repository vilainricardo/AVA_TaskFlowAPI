from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.models.task_types import TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.QUEUED)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: datetime | None = Field(default=None)
