# Backend README

This folder contains the FastAPI backend for the Smart Task Manager application.

## Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Environment variables

Copy `.env.example` to `.env` and fill in the values:

```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=SmartTaskManager
DATABASE_NAME=smart_task_manager
JWT_SECRET=your_secure_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:5173
```

## Run the API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security notes

- JWTs are validated on each protected request.
- Task access is restricted by authenticated user ownership.
- Users cannot read, update, or delete tasks that do not belong to them.
