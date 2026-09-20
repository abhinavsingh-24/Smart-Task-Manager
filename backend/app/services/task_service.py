from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from app.database import get_database
from app.schemas.task import TaskCreate, TaskUpdate


def _mongo_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.combine(value, datetime.min.time(), tzinfo=timezone.utc)


def _serialize_task(task: dict) -> dict:
    due_date = task.get("due_date")
    if isinstance(due_date, datetime):
        due_date = due_date.date().isoformat()

    return {
        "id": str(task["_id"]),
        "user_id": str(task["user_id"]),
        "title": task["title"],
        "description": task.get("description"),
        "status": task["status"],
        "priority": task["priority"],
        "due_date": due_date,
        "created_at": task["created_at"],
        "updated_at": task["updated_at"],
        "completed_at": task.get("completed_at"),
    }


def create_task(user_id: str, payload: TaskCreate) -> dict:
    db = get_database()
    now = datetime.now(timezone.utc)
    task_document = {
        "user_id": ObjectId(user_id),
        "title": payload.title.strip(),
        "description": payload.description.strip() if payload.description else None,
        "status": payload.status.lower(),
        "priority": payload.priority.lower(),
        "due_date": _mongo_datetime(payload.due_date),
        "created_at": now,
        "updated_at": now,
        "completed_at": now if payload.status.lower() == "completed" else None,
    }

    result = db.tasks.insert_one(task_document)
    created = db.tasks.find_one({"_id": result.inserted_id})
    return _serialize_task(created)


def list_tasks(user_id: str, *, page: int = 1, limit: int = 10, search: str | None = None, status: str | None = None, priority: str | None = None, sort: str = "newest") -> dict:
    db = get_database()
    query = {"user_id": ObjectId(user_id)}

    if status and status != "all":
        query["status"] = status
    if priority and priority != "all":
        query["priority"] = priority
    if search:
        search_term = search.strip()
        query["$or"] = [
            {"title": {"$regex": search_term, "$options": "i"}},
            {"description": {"$regex": search_term, "$options": "i"}},
        ]

    sort_map = {
        "newest": [("created_at", -1)],
        "oldest": [("created_at", 1)],
        "due_date": [("due_date", 1)],
        "priority": [("priority", -1)],
    }
    sort_field = sort_map.get(sort, sort_map["newest"])

    skip = (page - 1) * limit
    items = list(db.tasks.find(query).sort(sort_field).skip(skip).limit(limit))
    total = db.tasks.count_documents(query)

    return {
        "items": [_serialize_task(task) for task in items],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": max((total + limit - 1) // limit, 1) if total else 1,
    }


def get_task_by_id(user_id: str, task_id: str) -> dict:
    db = get_database()
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    if str(task["user_id"]) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this task.")
    return _serialize_task(task)


def update_task(user_id: str, task_id: str, payload: TaskUpdate) -> dict:
    db = get_database()
    existing = db.tasks.find_one({"_id": ObjectId(task_id)})
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    if str(existing["user_id"]) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this task.")

    existing = db.tasks.find_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    update_data = {}
    if payload.title is not None:
        update_data["title"] = payload.title.strip()
    if payload.description is not None:
        update_data["description"] = payload.description.strip() if payload.description else None
    if payload.status is not None:
        update_data["status"] = payload.status.lower()
    if payload.priority is not None:
        update_data["priority"] = payload.priority.lower()
    if payload.due_date is not None:
        update_data["due_date"] = _mongo_datetime(payload.due_date)

    if update_data.get("status") == "completed":
        update_data["completed_at"] = datetime.now(timezone.utc)
    elif existing.get("status") == "completed" and update_data.get("status") != "completed":
        update_data["completed_at"] = None

    update_data["updated_at"] = datetime.now(timezone.utc)

    db.tasks.update_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)}, {"$set": update_data})
    updated = db.tasks.find_one({"_id": ObjectId(task_id)})
    return _serialize_task(updated)


def delete_task(user_id: str, task_id: str) -> None:
    db = get_database()
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    if str(task["user_id"]) != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this task.")

    result = db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
