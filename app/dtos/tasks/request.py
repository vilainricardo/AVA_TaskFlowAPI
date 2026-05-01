from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.dtos.tasks.base import TaskBase
from app.models.task_types import TaskPriority, TaskStatus


class TaskCreateRequest(TaskBase):
    pass


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None)
    status: TaskStatus | None = Field(default=None)
    priority: TaskPriority | None = Field(default=None)
    due_date: datetime | None = Field(default=None)


class TaskFilterRequest(BaseModel):
    status: TaskStatus | None = Field(default=None)
    priority: TaskPriority | None = Field(default=None)
    text: str | None = Field(default=None, min_length=1)
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
