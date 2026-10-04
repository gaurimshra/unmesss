from sqlalchemy.orm import Session

from models import Task


def create_task(
    db: Session,
    title: str,
    description: str | None = None,
    deadline: str | None = None,
    priority: str = "normal",
    blocker: str | None = None,
):
    task = Task(
        title=title,
        description=description,
        deadline=deadline,
        priority=priority,
        blocker=blocker,
        status="pending",
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(db: Session):
    return db.query(Task).all()


def complete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    task.status = "completed"

    db.commit()
    db.refresh(task)

    return task
