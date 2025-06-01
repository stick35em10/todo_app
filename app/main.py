from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List

app = FastAPI()

class TaskStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class Task(BaseModel):
    id: int
    title: str
    status: TaskStatus

# Mock Database
tasks_db = [
    Task(id=1, title="Learn FastAPI", status=TaskStatus.TODO),
    Task(id=2, title="Deploy to Kubernetes", status=TaskStatus.DOING),
]

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.get("/tasks/{status}", response_model=List[Task])
def get_tasks_by_status(status: TaskStatus):
    return [task for task in tasks_db if task.status == status]

@app.put("/tasks/{task_id}/{new_status}")
def update_status(task_id: int, new_status: TaskStatus):
    task = next((t for t in tasks_db if t.id == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = new_status
    return {"message": "Status updated!"}