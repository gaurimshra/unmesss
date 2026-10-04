from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from agent import analyze_brain_dump
from pydantic import BaseModel

from database import Base, engine, get_db
from models import Task
from tools.task import create_task, get_tasks, complete_task
from fastapi.middleware.cors import CORSMiddleware
from tools.planner import get_next_task


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Unmesss API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BrainDumpRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "message": "Unmess backend is alive 🚀"
    }


@app.post("/tasks")
def add_task(
    title: str,
    deadline: str | None = None,
    priority: str = "normal",
    db: Session = Depends(get_db),
):
    return create_task(
        db=db,
        title=title,
        deadline=deadline,
        priority=priority,
    )


@app.get("/tasks")
def list_all_tasks(
    db: Session = Depends(get_db),
):

    tasks = get_tasks(db)

    return {
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "deadline": task.deadline,
                "priority": task.priority,
                "blocker": task.blocker,
                "status": task.status,
            }
            for task in tasks
        ]
    }

@app.patch("/tasks/{task_id}/complete")
def mark_complete(
    task_id: int,
    db: Session = Depends(get_db),
):

    task = complete_task(db, task_id)

    if not task:
        return {
            "error": "Task not found"
        }

    return {
        "id": task.id,
        "status": task.status
    }




@app.post("/brain-dump")
def brain_dump(
    request: BrainDumpRequest,
    db: Session = Depends(get_db),
):
    result = analyze_brain_dump(request.text)

    created_tasks = []

    for task_data in result["tasks"]:
        task = create_task(
            db=db,
            title=task_data["title"],
            description=task_data.get("description"),
            deadline=task_data.get("deadline"),
            priority=task_data.get("priority", "normal"),
            blocker=task_data.get("blocker"),
        )

        created_tasks.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline,
            "priority": task.priority,
            "blocker": task.blocker,
            "status": task.status,
        })

    return {
        "tasks": created_tasks
    }



@app.get("/next-task")
def next_task(
    db: Session = Depends(get_db),
):
    task = get_next_task(db)

    if not task:
        return {
            "message": "You're all caught up 🎉"
        }

    return {
        "task": task
    }
