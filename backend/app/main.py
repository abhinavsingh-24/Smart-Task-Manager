from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import connect_to_mongo
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router

app = FastAPI(
    title="Smart Task Manager API",
    description="API for managing tasks, users, authentication and dashboard data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings["ALLOWED_ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)


@app.on_event("startup")
def startup_event():
    """Initialize the MongoDB connection when the API starts."""
    try:
        connect_to_mongo()
    except RuntimeError as exc:
        app.state.db_error = str(exc)
    else:
        app.state.db_error = None


@app.get("/health")
def health_check():
    if getattr(app.state, "db_error", None):
        return {
            "status": "degraded",
            "message": app.state.db_error,
        }

    return {
        "status": "ok",
        "message": "Smart Task Manager backend is running.",
    }


@app.get("/")
def root():
    return {"message": "Welcome to Smart Task Manager API"}
