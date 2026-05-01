from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.dtos.tasks.base import TaskBase


class TaskCreateRequest(TaskBase):
    pass


class TaskUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None)
    completed: bool | None = Field(default=None)
    priority: int | None = Field(default=None, ge=1)
    due_date: datetime | None = Field(default=None)


class TaskFilterRequest(BaseModel):
    completed: bool | None = Field(default=None)
    priority: int | None = Field(default=None, ge=1)
    text: str | None = Field(default=None, min_length=1)


class TaskCompleteRequest(BaseModel):
    completed: bool = Field(default=True)


class TaskReopenRequest(BaseModel):
    completed: bool = Field(default=False)
