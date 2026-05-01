from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    completed: bool = Field(default=False)
    priority: int = Field(default=3, ge=1)
    due_date: datetime | None = Field(default=None)
