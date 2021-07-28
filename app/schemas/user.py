from pydantic.main import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    password: str


class UserReturn(BaseModel):
    id: int
    email: str