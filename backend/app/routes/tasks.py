from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.auth_service import get_current_user, security
from app.services.task_service import create_task, delete_task, get_task_by_id, list_tasks, update_task

router = APIRouter(prefix="/api", tags=["Tasks"])


@router.get(
    "/tasks",
    response_model=dict,
    summary="List tasks for the authenticated user",
    description="Return the current user's tasks with support for search, filters, sorting, and pagination.",
)
def get_tasks(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    sort: str = Query(default="newest"),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    current_user = get_current_user(credentials)
    tasks = list_tasks(
        current_user["id"],
        page=page,
        limit=limit,
        search=search,
        status=status,
        priority=priority,
        sort=sort,
    )
    return tasks


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
    description="Create a new task for the authenticated user with validation for status, priority, and due date.",
)
def create_new_task(payload: TaskCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_user = get_current_user(credentials)
    return create_task(current_user["id"], payload)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Get a single task",
    description="Fetch one task if it belongs to the authenticated user.",
)
def get_single_task(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_user = get_current_user(credentials)
    return get_task_by_id(current_user["id"], task_id)


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task owned by the authenticated user.",
)
def update_existing_task(
    task_id: str,
    payload: TaskUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    current_user = get_current_user(credentials)
    return update_task(current_user["id"], task_id, payload)


@router.delete(
    "/tasks/{task_id}",
    summary="Delete a task",
    description="Delete an existing task if it belongs to the authenticated user.",
)
def delete_existing_task(task_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    current_user = get_current_user(credentials)
    delete_task(current_user["id"], task_id)
    return {"message": "Task deleted successfully"}
