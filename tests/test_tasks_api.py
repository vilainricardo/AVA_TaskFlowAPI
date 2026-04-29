from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi.testclient import TestClient


def test_create_and_get_task(client: TestClient) -> None:
    payload: dict[str, object] = {
        "title": "API Task",
        "description": "Criada via router",
        "priority": 2,
        "due_date": datetime(2026, 4, 30, tzinfo=timezone.utc).isoformat(),
    }

    create_response = client.post("/api/v1/tasks", json=payload)

    assert create_response.status_code == 201
    body: dict[str, object] = create_response.json()
    task_id = UUID(str(body["id"]))
    assert body["title"] == "API Task"

    get_response = client.get(f"/api/v1/tasks/{task_id}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == str(task_id)


def test_list_update_complete_reopen_delete_task(client: TestClient) -> None:
    create_response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Task listada",
            "description": "Lista e altera",
            "priority": 3,
        },
    )
    task_id = str(create_response.json()["id"])

    list_response = client.get("/api/v1/tasks", params={"completed": False, "priority": 3, "text": "lista"})
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/api/v1/tasks/{task_id}",
        json={
            "title": "Task listada atualizada",
            "description": None,
            "priority": 4,
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Task listada atualizada"

    complete_response = client.patch(f"/api/v1/tasks/{task_id}/complete", json={"completed": True})
    assert complete_response.status_code == 200
    assert complete_response.json()["completed"] is True

    reopen_response = client.patch(f"/api/v1/tasks/{task_id}/reopen", json={"completed": False})
    assert reopen_response.status_code == 200
    assert reopen_response.json()["completed"] is False

    delete_response = client.delete(f"/api/v1/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_after_delete = client.get(f"/api/v1/tasks/{task_id}")
    assert get_after_delete.status_code == 404
