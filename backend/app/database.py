from pymongo import ASCENDING, MongoClient
from pymongo.errors import PyMongoError

from app.config import settings

client = None
db = None


def connect_to_mongo():
    global client, db

    mongo_uri = settings["MONGODB_URI"].strip()
    if not mongo_uri or "<db_password>" in mongo_uri:
        raise RuntimeError(
            "MONGODB_URI is not configured with a real Atlas connection string. "
            "Replace the placeholder value in backend/.env before starting the API."
        )

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        db = client[settings["DATABASE_NAME"]]
        client.admin.command("ping")
        ensure_database_indexes()
        return db
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB connection failed: {exc}") from exc


def get_database():
    if db is None:
        return connect_to_mongo()
    return db


def ensure_database_indexes():
    if db is None:
        raise RuntimeError("Database is not connected")

    db.users.create_index("email", unique=True, name="idx_users_email")
    db.tasks.create_index([("user_id", ASCENDING)], name="idx_tasks_user_id")
    db.tasks.create_index([("status", ASCENDING)], name="idx_tasks_status")
    db.tasks.create_index([("priority", ASCENDING)], name="idx_tasks_priority")
    db.tasks.create_index([("due_date", ASCENDING)], name="idx_tasks_due_date")
    db.tasks.create_index([("user_id", ASCENDING), ("due_date", ASCENDING)], name="idx_tasks_user_due_date")


def close_mongo_connection():
    global client, db
    if client is not None:
        client.close()
        client = None
    db = None
