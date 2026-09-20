from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from bson import ObjectId
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.database import get_database
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.security import hash_password, verify_password

security = HTTPBearer()


def create_user(payload: UserCreate) -> dict[str, Any]:
    db = get_database()
    if db.users.find_one({"email": payload.email.lower()}):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
        )

    now = datetime.now(timezone.utc)
    user_document = {
        "name": payload.name.strip(),
        "email": payload.email.lower(),
        "password_hash": hash_password(payload.password),
        "created_at": now,
        "updated_at": now,
    }

    result = db.users.insert_one(user_document)
    user_data = db.users.find_one({"_id": result.inserted_id})
    return {
        "id": str(user_data["_id"]),
        "name": user_data["name"],
        "email": user_data["email"],
        "created_at": user_data["created_at"],
        "updated_at": user_data["updated_at"],
    }


def authenticate_user(payload: UserLogin) -> dict[str, Any]:
    db = get_database()
    user = db.users.find_one({"email": payload.email.lower()})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    token = create_access_token(user_id=str(user["_id"]))
    user_response = UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        created_at=user["created_at"],
        updated_at=user["updated_at"],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_response,
    }


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings["ACCESS_TOKEN_EXPIRE_MINUTES"])
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, settings["JWT_SECRET"], algorithm=settings["JWT_ALGORITHM"])


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings["JWT_SECRET"], algorithms=[settings["JWT_ALGORITHM"]])
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Missing subject in token")
        return str(user_id)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from exc


def get_current_user(credentials: HTTPAuthorizationCredentials = None) -> dict[str, Any]:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    user_id = decode_access_token(credentials.credentials)
    db = get_database()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at"),
    }
