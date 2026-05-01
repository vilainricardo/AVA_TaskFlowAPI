from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_types import TaskPriority, TaskStatus


class TaskRepository:
    def _apply_filters(
        self,
        statement: Select[tuple[Task]],
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        text: str | None = None,
    ) -> Select[tuple[Task]]:
        if status is not None:
            statement = statement.where(Task.status == status)
        if priority is not None:
            statement = statement.where(Task.priority == priority)
        if text is not None:
            pattern: str = f"%{text.lower()}%"
            statement = statement.where(
                or_(
                    func.lower(Task.title).like(pattern),
                    func.lower(Task.description).like(pattern),
                )
            )
        return statement

    def list(
        self,
        session: Session,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        text: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[Task]:
        statement: Select[tuple[Task]] = select(Task)
        statement = self._apply_filters(
            statement,
            status=status,
            priority=priority,
            text=text,
        )
        statement = statement.order_by(Task.created_at.desc())
        if offset is not None:
            statement = statement.offset(offset)
        if limit is not None:
            statement = statement.limit(limit)
        result = session.execute(statement)
        return list(result.scalars().all())

    def count(
        self,
        session: Session,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        text: str | None = None,
    ) -> int:
        statement = select(func.count(Task.id))
        statement = self._apply_filters(
            statement,
            status=status,
            priority=priority,
            text=text,
        )
        result = session.execute(statement)
        return int(result.scalar_one())

    def get_by_id(self, session: Session, task_id: UUID) -> Task | None:
        statement: Select[tuple[Task]] = select(Task).where(Task.id == task_id)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def add(self, session: Session, task: Task) -> Task:
        session.add(task)
        session.flush()
        return task

    def delete(self, session: Session, task: Task) -> None:
        session.delete(task)
        session.flush()
