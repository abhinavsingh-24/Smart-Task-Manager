from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name is required.")
        return value.strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password confirmation must be at least 8 characters long.")
        return value

    @property
    def password_matches(self) -> bool:
        return self.password == self.confirm_password

    @property
    def is_valid(self) -> bool:
        return self.password_matches


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
