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
    """EN: Create the TaskService dependency used by task endpoints.
    PT-BR: Cria a dependencia TaskService usada pelos endpoints de tarefa.
    """

    return TaskService()


def _raise_not_found_error(error: TaskNotFoundError) -> None:
    """EN: Convert a domain not-found error into an HTTP 404 response.
    PT-BR: Converte um erro de inexistencia em resposta HTTP 404.
    """

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error),
    ) from error


@router.post(
    "",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create task / Criar tarefa",
    description=(
        "EN: Create a new task from validated input data and return the persisted record.\n"
        "PT-BR: Cria uma nova tarefa a partir de dados validados e retorna o registro persistido.\n\n"
        "Input / Entrada: TaskCreate payload.\n"
        "Output / Saida: TaskRead representation with id and timestamps."
    ),
    response_description="Created task / Tarefa criada",
)
def create_task(
    payload: TaskCreate,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    """EN: Create a task and return the API read model.
    PT-BR: Cria uma tarefa e retorna o model de leitura da API.
    """

    task = service.create_task(session, payload)
    return TaskRead.model_validate(task)


@router.get(
    "",
    response_model=list[TaskRead],
    summary="List tasks / Listar tarefas",
    description=(
        "EN: Return tasks filtered by completion, priority, and text search.\n"
        "PT-BR: Retorna tarefas filtradas por conclusao, prioridade e busca textual.\n\n"
        "Input / Entrada: Query filters TaskFilter.\n"
        "Output / Saida: List of TaskRead items."
    ),
    response_description="Task list / Lista de tarefas",
)
def list_tasks(
    filters: Annotated[TaskFilter, Depends()],
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskRead]:
    """EN: List tasks using query filters.
    PT-BR: Lista tarefas usando filtros de consulta.
    """

    tasks = service.list_tasks(session, filters)
    return [TaskRead.model_validate(task) for task in tasks]


@router.get(
    "/{task_id}",
    response_model=TaskRead,
    summary="Get task / Consultar tarefa",
    description=(
        "EN: Fetch a single task by its UUID identifier.\n"
        "PT-BR: Busca uma unica tarefa pelo identificador UUID.\n\n"
        "Input / Entrada: task_id path parameter.\n"
        "Output / Saida: TaskRead if found, otherwise 404."
    ),
    response_description="Task details / Detalhes da tarefa",
)
def get_task(
    task_id: UUID,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    """EN: Read a task by id and return it to the client.
    PT-BR: Le uma tarefa pelo id e a retorna ao cliente.
    """

    try:
        task = service.get_task(session, task_id)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskRead,
    summary="Update task / Atualizar tarefa",
    description=(
        "EN: Replace mutable task fields using validated input data.\n"
        "PT-BR: Atualiza campos mutaveis da tarefa usando dados validados.\n\n"
        "Input / Entrada: task_id path parameter and TaskUpdate body.\n"
        "Output / Saida: Updated TaskRead or 404."
    ),
    response_description="Updated task / Tarefa atualizada",
)
def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    """EN: Update a task and return the updated record.
    PT-BR: Atualiza uma tarefa e retorna o registro atualizado.
    """

    try:
        task = service.update_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.patch(
    "/{task_id}/complete",
    response_model=TaskRead,
    summary="Complete task / Concluir tarefa",
    description=(
        "EN: Mark a task as completed using the completion payload.\n"
        "PT-BR: Marca uma tarefa como concluida usando o payload de conclusao.\n\n"
        "Input / Entrada: task_id path parameter and TaskComplete body.\n"
        "Output / Saida: Updated TaskRead or 404."
    ),
    response_description="Completed task / Tarefa concluida",
)
def complete_task(
    task_id: UUID,
    payload: TaskComplete,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    """EN: Complete a task and return the updated record.
    PT-BR: Conclui uma tarefa e retorna o registro atualizado.
    """

    try:
        task = service.complete_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.patch(
    "/{task_id}/reopen",
    response_model=TaskRead,
    summary="Reopen task / Reabrir tarefa",
    description=(
        "EN: Reopen a completed task using the reopen payload.\n"
        "PT-BR: Reabre uma tarefa concluida usando o payload de reabertura.\n\n"
        "Input / Entrada: task_id path parameter and TaskReopen body.\n"
        "Output / Saida: Updated TaskRead or 404."
    ),
    response_description="Reopened task / Tarefa reaberta",
)
def reopen_task(
    task_id: UUID,
    payload: TaskReopen,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    """EN: Reopen a task and return the updated record.
    PT-BR: Reabre uma tarefa e retorna o registro atualizado.
    """

    try:
        task = service.reopen_task(session, task_id, payload)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return TaskRead.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task / Excluir tarefa",
    description=(
        "EN: Delete a task by UUID and return no content.\n"
        "PT-BR: Exclui uma tarefa pelo UUID e nao retorna conteudo.\n\n"
        "Input / Entrada: task_id path parameter.\n"
        "Output / Saida: HTTP 204 No Content."
    ),
    response_description="No content / Sem conteudo",
)
def delete_task(
    task_id: UUID,
    session: Annotated[Session, Depends(get_db)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> Response:
    """EN: Delete a task from persistence.
    PT-BR: Exclui uma tarefa da persistencia.
    """

    try:
        service.delete_task(session, task_id)
    except TaskNotFoundError as error:
        _raise_not_found_error(error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
