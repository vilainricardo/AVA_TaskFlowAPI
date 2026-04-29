from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas import (
    TaskComplete,
    TaskCreate,
    TaskFilter,
    TaskRead,
    TaskReopen,
    TaskUpdate,
)
from app.services import TaskNotFoundError, TaskService

router: APIRouter = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service() -> TaskService:
    return TaskService()


def _raise_not_found_error(error: TaskNotFoundError) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error),
    ) from error


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    task = service.create_task(session, payload)
    return TaskRead.model_validate(task)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    filters: Annotated[TaskFilter, Depends()],
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskRead]:
    tasks = service.list_tasks(session, filters)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        task = service.get_task(session, task_id)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        task = service.update_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: UUID,
    payload: TaskComplete,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        task = service.complete_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.patch("/{task_id}/reopen", response_model=TaskRead)
def reopen_task(
    task_id: UUID,
    payload: TaskReopen,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        task = service.reopen_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> Response:
    try:
        service.delete_task(session, task_id)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
