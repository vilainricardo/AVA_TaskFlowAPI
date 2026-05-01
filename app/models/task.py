from __future__ import annotations

from datetime import datetime, timezone
from typing import ClassVar
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum as SAEnum, Index, String, Text, text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.task_types import TaskPriority, TaskStatus


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Task(Base):
    __tablename__: ClassVar[str] = "tasks"
    __table_args__: ClassVar[tuple[Index, ...]] = (
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_priority", "priority"),
        Index("idx_tasks_due_date", "due_date"),
        Index("idx_tasks_created_at", "created_at"),
    )

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(
            TaskStatus,
            name="task_status",
            native_enum=False,
            create_constraint=True,
            length=20,
        ),
        nullable=False,
        default=TaskStatus.QUEUED,
        server_default=text("'queued'"),
    )
    priority: Mapped[TaskPriority] = mapped_column(
        SAEnum(
            TaskPriority,
            name="task_priority",
            native_enum=False,
            create_constraint=True,
            length=20,
        ),
        nullable=False,
        default=TaskPriority.MEDIUM,
        server_default=text("'medium'"),
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=text("timezone('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=text("timezone('utc', now())"),
    )
