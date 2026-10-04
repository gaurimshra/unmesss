from sqlalchemy.orm import Session
from models import Task


PRIORITY_SCORE = {
    "critical": 4,
    "high": 3,
    "normal": 2,
    "low": 1,
}


def get_next_task(db: Session):

    tasks = (
        db.query(Task)
        .filter(Task.status == "pending")
        .all()
    )

    if not tasks:
        return None

    tasks.sort(
        key=lambda task: PRIORITY_SCORE.get(
            task.priority,
            1
        ),
        reverse=True,
    )

    return tasks[0]
