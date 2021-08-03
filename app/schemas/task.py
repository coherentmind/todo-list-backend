from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    task_name: str


class TaskCreateExtended(TaskCreate):
    owner_id: int


class TaskUpdate(BaseModel):
    task_name: str
    completeness: bool


class TaskReturn(BaseModel):
    id: int
    task_name: str
    completeness: bool
    creation_date: datetime
    owner_id: int