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
    assert len(body["detail"]) >= 1


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
    assert len(list_response.json()) == 1

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


def test_mutation_endpoints_return_404_for_missing_task(client: TestClient) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"

    update_response = client.put(
        f"/api/v1/tasks/{missing_id}",
        json={"title": "Nao existe"},
    )
    assert update_response.status_code == 404

    complete_response = client.patch(f"/api/v1/tasks/{missing_id}/complete")
    assert complete_response.status_code == 404

    reopen_response = client.patch(f"/api/v1/tasks/{missing_id}/reopen")
    assert reopen_response.status_code == 404

    delete_response = client.delete(f"/api/v1/tasks/{missing_id}")
    assert delete_response.status_code == 404
