from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.task import TASK_PRIORITY_VALUES, TASK_STATUS_VALUES


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: str = Field(default="pending")
    priority: str = Field(default="medium")
    due_date: date | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        status = value.strip().lower()
        if status not in TASK_STATUS_VALUES:
            raise ValueError("Status must be one of: pending, in_progress, completed")
        return status

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str) -> str:
        priority = value.strip().lower()
        if priority not in TASK_PRIORITY_VALUES:
            raise ValueError("Priority must be one of: low, medium, high")
        return priority

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Task title is required.")
        return value.strip()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: str | None = Field(default=None)
    priority: str | None = Field(default=None)
    due_date: date | None = None


class TaskResponse(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
