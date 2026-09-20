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


def test_register_user(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    }

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["user"]["email"] == "alice@example.com"
    assert "password" not in data["user"]


def test_duplicate_registration(client):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!",
    }
    client.post("/api/auth/register", json=payload)

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409


def test_login_user(client):
    client.post(
        "/api/auth/register",
        json={
            "name": "Bob",
            "email": "bob@example.com",
            "password": "StrongPass123!",
            "confirm_password": "StrongPass123!",
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "bob@example.com",
            "password": "StrongPass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "missing@example.com",
            "password": "WrongPass123!",
        },
    )
    assert response.status_code == 401


def test_missing_token(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_invalid_token(client):
    response = client.get("/api/tasks", headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
