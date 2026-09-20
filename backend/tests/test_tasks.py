import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_database

pytestmark = pytest.mark.skipif(
    not os.getenv("MONGODB_URI", "").strip() or "<db_password>" in os.getenv("MONGODB_URI", ""),
    reason="MongoDB Atlas credentials are not configured with a real URI.",
)


@pytest.fixture
def client():
    db = get_database()
    db.users.delete_many({})
    db.tasks.delete_many({})
    with TestClient(app) as test_client:
        yield test_client


def register_user(client, email="user@example.com", password="StrongPass123!"):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )
    assert response.status_code == 201
    return response.json()["user"]


def login_user(client, email="user@example.com", password="StrongPass123!"):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_and_get_tasks(client):
    register_user(client)
    token = login_user(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/tasks",
        json={
            "title": "Prepare portfolio",
            "description": "Update the resume and GitHub repo",
            "status": "pending",
            "priority": "high",
            "due_date": "2026-10-01",
        },
        headers=headers,
    )
    assert response.status_code == 201

    tasks_response = client.get("/api/tasks", headers=headers)
    assert tasks_response.status_code == 200
    data = tasks_response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Prepare portfolio"


def test_get_single_task_and_update(client):
    register_user(client, email="one@example.com")
    token = login_user(client, email="one@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/tasks",
        json={
            "title": "Practice Python",
            "description": "Solve interview questions",
            "status": "in_progress",
            "priority": "medium",
            "due_date": "2026-10-02",
        },
        headers=headers,
    )
    task_id = created.json()["id"]

    single = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert single.status_code == 200

    updated = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Practice Python deeply", "status": "completed"},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Practice Python deeply"
    assert updated.json()["status"] == "completed"


def test_unauthorized_task_access(client):
    register_user(client, email="user1@example.com")
    register_user(client, email="user2@example.com")
    token1 = login_user(client, email="user1@example.com")
    token2 = login_user(client, email="user2@example.com")

    created = client.post(
        "/api/tasks",
        json={
            "title": "User 1 task",
            "status": "pending",
            "priority": "low",
            "due_date": "2026-10-04",
        },
        headers={"Authorization": f"Bearer {token1}"},
    )
    task_id = created.json()["id"]

    forbidden = client.get(f"/api/tasks/{task_id}", headers={"Authorization": f"Bearer {token2}"})
    assert forbidden.status_code == 403


def test_search_and_filter_and_pagination(client):
    register_user(client, email="search@example.com")
    token = login_user(client, email="search@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    for i in range(3):
        client.post(
            "/api/tasks",
            json={
                "title": f"Task {i} interview prep",
                "description": "Focus on Python challenge" if i % 2 else "Focus on resume",
                "status": "pending" if i == 0 else "completed",
                "priority": "high" if i == 0 else "medium",
                "due_date": "2026-10-0{}".format(i + 1),
            },
            headers=headers,
        )

    search_response = client.get("/api/tasks?search=interview&status=pending", headers=headers)
    assert search_response.status_code == 200
    assert search_response.json()["total"] == 1

    page_response = client.get("/api/tasks?page=1&limit=2", headers=headers)
    assert page_response.status_code == 200
    assert page_response.json()["page"] == 1
    assert page_response.json()["limit"] == 2


def test_delete_task(client):
    register_user(client, email="delete@example.com")
    token = login_user(client, email="delete@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/tasks",
        json={
            "title": "Delete me",
            "status": "pending",
            "priority": "low",
            "due_date": "2026-10-05",
        },
        headers=headers,
    )
    task_id = created.json()["id"]

    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"
