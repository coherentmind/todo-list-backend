from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    name: str


class TaskCreateExtended(TaskCreate):
    owner_id: int


class TaskUpdate(BaseModel):
    name: str
    completness: bool


class TaskReturn(BaseModel):
    id: int
    name: str
    completness: bool
    date: datetime