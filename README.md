# Smart Task Manager

A secure full-stack task management application built with React, FastAPI, and MongoDB Atlas. It supports JWT authentication, protected task ownership, filtering, search, pagination, and a clean dashboard UI.

## Project status

This project is complete and verified for the core portfolio workflow:
- React frontend with login/register flow and protected routes
- FastAPI backend with MongoDB integration
- JWT authentication and password hashing
- Task CRUD with ownership enforcement to prevent IDOR/BOLA issues
- Backend tests and frontend build verification

## Stack

- Frontend: React + Vite + JavaScript
- Backend: Python + FastAPI
- Database: MongoDB Atlas
- Auth: JWT + bcrypt
- Testing: pytest + Vitest

## Repository structure

```text
smart-task-manager/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env
│   └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js
│   ├── .env.example
│   └── .env
├── .gitignore
├── README.md
├── LICENSE
└── .venv/
```

## Local setup

### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set your values:

```env
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/?appName=SmartTaskManager
DATABASE_NAME=smart_task_manager
JWT_SECRET=your_secure_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:5173
```

Run the API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
```

Create a local `.env` file based on `.env.example`:

```env
VITE_API_URL=http://localhost:8000
```

Run the app:

```bash
npm run dev
```

## App features

- User registration and login
- JWT-based session persistence
- Protected dashboard and task routes
- Task creation, editing, deletion, search, sorting, and pagination
- Role-safe task ownership checks so users can only access their own tasks

## API docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Verification

The project was verified with fresh checks:
- Backend: `11 passed` via pytest
- Frontend: `npm run build` succeeded with Vite

## Notes

- Keep `.env` files local and do not commit secrets.
- MongoDB Atlas credentials must be supplied in the backend `.env` file for live database connectivity.
