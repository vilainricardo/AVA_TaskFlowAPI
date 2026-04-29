from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_audit import TaskAudit
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskComplete, TaskCreate, TaskFilter, TaskRead, TaskReopen, TaskUpdate


class TaskNotFoundError(Exception):
    pass


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TaskService:
    def __init__(self) -> None:
        self._repository: TaskRepository = TaskRepository()

    def _serialize_task(self, task: Task) -> dict[str, Any]:
        return TaskRead.model_validate(task).model_dump(mode="json")

    def _create_audit(
        self,
        session: Session,
        *,
        task_id: UUID,
        action: str,
        before_state: dict[str, Any] | None,
        after_state: dict[str, Any] | None,
    ) -> TaskAudit:
        audit: TaskAudit = TaskAudit(
            task_id=task_id,
            action=action,
            before_state=before_state,
            after_state=after_state,
        )
        session.add(audit)
        session.flush()
        return audit

    def _get_task_or_raise(self, session: Session, task_id: UUID) -> Task:
        task: Task | None = self._repository.get_by_id(session, task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def create_task(self, session: Session, payload: TaskCreate) -> Task:
        task: Task = Task(
            title=payload.title,
            description=payload.description,
            completed=payload.completed,
            priority=payload.priority,
            due_date=payload.due_date,
        )
        self._repository.add(session, task)
        self._create_audit(
            session,
            task_id=task.id,
            action="CREATE",
            before_state=None,
            after_state=self._serialize_task(task),
        )
        session.commit()
        session.refresh(task)
        return task

    def list_tasks(self, session: Session, filters: TaskFilter) -> list[Task]:
        return self._repository.list(
            session,
            completed=filters.completed,
            priority=filters.priority,
            text=filters.text,
        )

    def get_task(self, session: Session, task_id: UUID) -> Task:
        return self._get_task_or_raise(session, task_id)

    def update_task(self, session: Session, task_id: UUID, payload: TaskUpdate) -> Task:
        task: Task = self._get_task_or_raise(session, task_id)
        before_state: dict[str, Any] = self._serialize_task(task)

        updates: dict[str, Any] = payload.model_dump(exclude_unset=True)
        for field_name, field_value in updates.items():
            setattr(task, field_name, field_value)

        task.updated_at = utc_now()
        session.flush()
        self._create_audit(
            session,
            task_id=task.id,
            action="UPDATE",
            before_state=before_state,
            after_state=self._serialize_task(task),
        )
        session.commit()
        session.refresh(task)
        return task

    def complete_task(self, session: Session, task_id: UUID, payload: TaskComplete) -> Task:
        task: Task = self._get_task_or_raise(session, task_id)
        before_state: dict[str, Any] = self._serialize_task(task)
        task.completed = payload.completed
        task.updated_at = utc_now()
        session.flush()
        self._create_audit(
            session,
            task_id=task.id,
            action="COMPLETE",
            before_state=before_state,
            after_state=self._serialize_task(task),
        )
        session.commit()
        session.refresh(task)
        return task

    def reopen_task(self, session: Session, task_id: UUID, payload: TaskReopen) -> Task:
        task: Task = self._get_task_or_raise(session, task_id)
        before_state: dict[str, Any] = self._serialize_task(task)
        task.completed = payload.completed
        task.updated_at = utc_now()
        session.flush()
        self._create_audit(
            session,
            task_id=task.id,
            action="REOPEN",
            before_state=before_state,
            after_state=self._serialize_task(task),
        )
        session.commit()
        session.refresh(task)
        return task

    def delete_task(self, session: Session, task_id: UUID) -> None:
        task: Task = self._get_task_or_raise(session, task_id)
        before_state: dict[str, Any] = self._serialize_task(task)
        self._create_audit(
            session,
            task_id=task.id,
            action="DELETE",
            before_state=before_state,
            after_state=None,
        )
        self._repository.delete(session, task)
        session.commit()
