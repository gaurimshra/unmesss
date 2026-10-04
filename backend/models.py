from sqlalchemy import Column, Integer, String, Boolean, Text
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    deadline = Column(String, nullable=True)

    priority = Column(String, default="normal")

    status = Column(String, default="pending")

    blocker = Column(String, nullable=True)