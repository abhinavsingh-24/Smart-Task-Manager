import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@lru_cache(maxsize=1)
def get_settings():
    return {
        "MONGODB_URI": os.getenv("MONGODB_URI", ""),
        "DATABASE_NAME": os.getenv("DATABASE_NAME", "smart_task_manager"),
        "JWT_SECRET": os.getenv("JWT_SECRET", "change-me-in-production"),
        "JWT_ALGORITHM": os.getenv("JWT_ALGORITHM", "HS256"),
        "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        "ALLOWED_ORIGINS": [
            origin.strip()
            for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
            if origin.strip()
        ],
    }


settings = get_settings()
