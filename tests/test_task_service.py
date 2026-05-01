from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.dtos.tasks import (
    TaskCompleteRequest,
    TaskCreateRequest,
    TaskFilterRequest,
    TaskReopenRequest,
    TaskUpdateRequest,
)
from app.models.task import Task
from app.models.task_audit import TaskAudit
from app.repositories import TaskRepository
from app.services import TaskNotFoundError, TaskService


def test_create_task_persists_task_and_audit(db_session: Session) -> None:
    service: TaskService = TaskService()
    payload: TaskCreateRequest = TaskCreateRequest(
        title="Implementar API",
        description="Criar endpoints principais",
        priority=2,
        due_date=datetime(2026, 4, 30, tzinfo=timezone.utc),
    )

    task: Task = service.create_task(db_session, payload)

    assert isinstance(task.id, UUID)
    assert task.title == "Implementar API"
    assert task.completed is False

    audits: list[TaskAudit] = db_session.query(TaskAudit).order_by(TaskAudit.created_at.asc()).all()
    assert len(audits) == 1
    assert audits[0].action == "CREATE"


def test_list_tasks_with_filters(db_session: Session) -> None:
    service: TaskService = TaskService()
    repository: TaskRepository = TaskRepository()

    service.create_task(
        db_session,
        TaskCreateRequest(title="Task Alpha", description="Primeira", completed=False, priority=1),
    )
    service.create_task(
        db_session,
        TaskCreateRequest(title="Task Beta", description="Segunda", completed=True, priority=3),
    )

    tasks: list[Task] = repository.list(db_session, completed=True, priority=3, text="beta")

    assert len(tasks) == 1
    assert tasks[0].title == "Task Beta"


def test_update_complete_reopen_and_delete_task(db_session: Session) -> None:
    service: TaskService = TaskService()
    task: Task = service.create_task(db_session, TaskCreateRequest(title="Task", description="Original"))

    updated: Task = service.update_task(
        db_session,
        task.id,
        TaskUpdateRequest(title="Task Atualizada", description=None, priority=5),
    )
    assert updated.title == "Task Atualizada"
    assert updated.description is None
    assert updated.priority == 5

    completed: Task = service.complete_task(db_session, task.id, TaskCompleteRequest())
    assert completed.completed is True

    reopened: Task = service.reopen_task(db_session, task.id, TaskReopenRequest())
    assert reopened.completed is False

    service.delete_task(db_session, task.id)
    remaining: list[Task] = service.list_tasks(db_session, TaskFilterRequest())
    assert len(remaining) == 0


def test_get_task_raises_not_found(db_session: Session) -> None:
    service: TaskService = TaskService()

    try:
        service.get_task(db_session, UUID("00000000-0000-0000-0000-000000000000"))
    except TaskNotFoundError as error:
        assert "not found" in str(error)
    else:
        raise AssertionError("TaskNotFoundError was not raised")
