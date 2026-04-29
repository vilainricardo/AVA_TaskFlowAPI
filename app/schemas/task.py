from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    priority: int = Field(default=3, ge=1)
    due_date: datetime | None = Field(default=None)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None)
    completed: bool | None = Field(default=None)
    priority: int | None = Field(default=None, ge=1)
    due_date: datetime | None = Field(default=None)


class TaskFilter(BaseModel):
    completed: bool | None = Field(default=None)
    priority: int | None = Field(default=None, ge=1)
    text: str | None = Field(default=None, min_length=1)


class TaskComplete(BaseModel):
    completed: bool = Field(default=True)


class TaskReopen(BaseModel):
    completed: bool = Field(default=False)


class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
