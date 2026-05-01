from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi.testclient import TestClient


def test_create_and_get_task(client: TestClient) -> None:
    payload: dict[str, object] = {
        "title": "API Task",
        "description": "Criada via router",
        "priority": "high",
        "status": "queued",
        "due_date": datetime(2026, 4, 30, tzinfo=timezone.utc).isoformat(),
    }

    create_response = client.post("/api/v1/tasks", json=payload)

    assert create_response.status_code == 201
    body: dict[str, object] = create_response.json()
    task_id = UUID(str(body["id"]))
    assert body["title"] == "API Task"
    assert body["status"] == "queued"

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == str(task_id)


def test_create_task_rejects_invalid_payload(client: TestClient) -> None:
    response = client.post(
        "/api/v1/tasks",
        json={
            "description": "Sem titulo",
            "priority": "invalid",
        },
    )

    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    error_fields: set[str] = {error["field"] for error in body["error"]["details"]}
    assert "title" in error_fields
    assert "priority" in error_fields


def test_list_update_complete_reopen_delete_task(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task listada",
            "description": "Lista e altera",
            "priority": "high",
            "status": "queued",
        },
    )
    task_id = str(create_response.json()["id"])

    list_response = client.get("/api/v1/tasks", params={"status": "queued", "priority": "high", "text": "lista"})
    assert list_response.status_code == 200
    list_body = list_response.json()
    assert len(list_body["items"]) == 1
    assert list_body["pagination"]["total"] == 1
    assert list_body["pagination"]["limit"] == 20
    assert list_body["pagination"]["offset"] == 0
    assert list_body["pagination"]["has_next"] is False

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Task listada atualizada",
            "description": None,
            "status": "in_progress",
            "priority": "urgent",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Task listada atualizada"
    assert update_response.json()["status"] == "in_progress"

    complete_response = client.patch(f"/api/v1/tasks/{task_id}/complete")
    assert complete_response.status_code == 200
    assert complete_response.json()["status"] == "completed"

    reopen_response = client.patch(f"/api/v1/tasks/{task_id}/reopen")
    assert reopen_response.status_code == 200
    assert reopen_response.json()["status"] == "queued"

    delete_response = client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_after_delete = client.get(f"/api/v1/tasks/{task_id}")
    assert get_after_delete.status_code == 404
    assert get_after_delete.json()["error"]["code"] == "TASK_NOT_FOUND"


def test_mutation_endpoints_return_404_for_missing_task(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"

    update_response = client.put(
        f"/api/v1/tasks/{missing_id}",
        json={"title": "Nao existe"},
    )
    assert update_response.status_code == 404
    assert update_response.json()["error"]["code"] == "TASK_NOT_FOUND"

    complete_response = client.patch(f"/api/v1/tasks/{missing_id}/complete")
    assert complete_response.status_code == 404
    assert complete_response.json()["error"]["code"] == "TASK_NOT_FOUND"

    reopen_response = client.patch(f"/api/v1/tasks/{missing_id}/reopen")
    assert reopen_response.status_code == 404
    assert reopen_response.json()["error"]["code"] == "TASK_NOT_FOUND"

    delete_response = client.delete(f"/api/v1/tasks/{missing_id}")
    assert delete_response.status_code == 404
    assert delete_response.json()["error"]["code"] == "TASK_NOT_FOUND"


def test_get_task_returns_404_for_missing_task(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/api/v1/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TASK_NOT_FOUND"
    assert response.json()["error"]["message"] == "Task not found."


def test_get_task_rejects_invalid_uuid(client: TestClient) -> None:
    response = client.get("/api/v1/tasks/not-a-uuid")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    error_fields: set[str] = {error["field"] for error in response.json()["error"]["details"]}
    assert "task_id" in error_fields


def test_list_tasks_rejects_empty_text_filter(client: TestClient) -> None:
    response = client.get("/api/v1/tasks", params={"text": ""})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    error_fields: set[str] = {error["field"] for error in response.json()["error"]["details"]}
    assert "text" in error_fields


def test_list_tasks_supports_limit_and_offset(client: TestClient) -> None:
    for index in range(3):
        response = client.post(
            "/api/v1/tasks",
            json={"title": f"Task {index}", "description": "Paginacao"},
        )
        assert response.status_code == 201

    page_response = client.get("/api/v1/tasks", params={"limit": 2, "offset": 1})
    assert page_response.status_code == 200
    body = page_response.json()
    assert len(body["items"]) == 2
    assert body["pagination"]["limit"] == 2
    assert body["pagination"]["offset"] == 1
    assert body["pagination"]["total"] == 3
    assert body["pagination"]["has_next"] is False


def test_list_tasks_rejects_invalid_pagination_params(client: TestClient) -> None:
    response = client.get("/api/v1/tasks", params={"limit": 0, "offset": -1})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
    error_fields: set[str] = {error["field"] for error in response.json()["error"]["details"]}
    assert "limit" in error_fields
    assert "offset" in error_fields


def test_reopen_returns_409_when_task_not_completed(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={"title": "Nao concluida", "description": "", "priority": "medium"},
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    reopen_response = client.patch(f"/api/v1/tasks/{task_id}/reopen")
    assert reopen_response.status_code == 409
    body = reopen_response.json()
    assert body["error"]["code"] == "TASK_REOPEN_REQUIRES_COMPLETED"
    assert body["error"]["message"] == "Only completed tasks can be reopened."
