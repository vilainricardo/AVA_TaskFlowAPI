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
    """EN: Raised when a task cannot be found.
    PT-BR: Lanca-se quando uma tarefa nao pode ser encontrada.
    """

    pass


def utc_now() -> datetime:
    """EN: Return the current UTC datetime.
    PT-BR: Retorna a data e hora atual em UTC.
    """

    return datetime.now(timezone.utc)


class TaskService:
    """EN: Service layer for task business rules and audit logging.
    PT-BR: Camada de servico para regras de negocio de tarefas e registro de auditoria.
    """

    def __init__(self) -> None:
        """EN: Build a TaskService with its repository dependency.
        PT-BR: Cria um TaskService com sua dependencia de repository.
        """

        self._repository: TaskRepository = TaskRepository()

    def _serialize_task(self, task: Task) -> dict[str, Any]:
        """EN: Convert a Task model into a JSON-safe dictionary.
        PT-BR: Converte um model Task em um dicionario seguro para JSON.
        """

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
        """EN: Persist an audit row for a task mutation.
        PT-BR: Persiste uma linha de auditoria para uma mutacao de tarefa.

        Args:
            session: Active SQLAlchemy session used for persistence.
            task_id: Task identifier related to the audit entry.
            action: Action name that describes the change.
            before_state: Serialized state before the change.
            after_state: Serialized state after the change.

        Returns:
            TaskAudit: The persisted audit record.
        """

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
        """EN: Load a task by id or raise TaskNotFoundError.
        PT-BR: Carrega uma tarefa pelo id ou dispara TaskNotFoundError.
        """

        task: Task | None = self._repository.get_by_id(session, task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def create_task(self, session: Session, payload: TaskCreate) -> Task:
        """EN: Create a task and store its initial audit entry.
        PT-BR: Cria uma tarefa e grava sua entrada inicial de auditoria.

        Args:
            session: Active SQLAlchemy session.
            payload: Validated task creation data.

        Returns:
            Task: The persisted task.
        """

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
        """EN: Return tasks filtered by status, priority, and text.
        PT-BR: Retorna tarefas filtradas por status, prioridade e texto.

        Args:
            session: Active SQLAlchemy session.
            filters: Query filters from the API layer.

        Returns:
            list[Task]: Matching tasks ordered by creation date.
        """

        return self._repository.list(
            session,
            completed=filters.completed,
            priority=filters.priority,
            text=filters.text,
        )

    def get_task(self, session: Session, task_id: UUID) -> Task:
        """EN: Fetch a task by id.
        PT-BR: Busca uma tarefa pelo id.
        """

        return self._get_task_or_raise(session, task_id)

    def update_task(self, session: Session, task_id: UUID, payload: TaskUpdate) -> Task:
        """EN: Update mutable task fields and store an audit record.
        PT-BR: Atualiza campos mutaveis da tarefa e armazena auditoria.
        """

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
        """EN: Mark a task as completed and audit the transition.
        PT-BR: Marca uma tarefa como concluida e audita a transicao.
        """

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
        """EN: Reopen a completed task and audit the transition.
        PT-BR: Reabre uma tarefa concluida e audita a transicao.
        """

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
        """EN: Delete a task and persist a delete audit entry.
        PT-BR: Exclui uma tarefa e persiste uma auditoria de exclusao.
        """

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
