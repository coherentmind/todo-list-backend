from uuid import UUID
from fastapi_utils.api_model import APIModel
from pydantic.main import BaseModel


class UserCreate(BaseModel):
    nickname: str
    password: str


class UserUpdate(BaseModel):
    password: str


class UserReturn(BaseModel):
    id: UUID
    nickname: str