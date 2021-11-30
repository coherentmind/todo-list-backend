from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from mysql.connector import MySQLConnection

_CreateType = TypeVar("_CreateType")
_UpdateType = TypeVar("_UpdateType")
_ReturnType = TypeVar("_ReturnType")


class BaseCRUD(ABC, Generic[_CreateType, _UpdateType, _ReturnType]):
    @abstractmethod
    def get(self, db: MySQLConnection, *, id: int) -> Optional[_ReturnType]:
        ...

    @abstractmethod
    def get_multi(self, db: MySQLConnection) -> list[_ReturnType]:
        ...

    @abstractmethod
    def create(self, db: MySQLConnection, *, data: _CreateType) -> _ReturnType:
        ...

    @abstractmethod
    def update(self, db: MySQLConnection, *, id: int, data: _UpdateType) -> None:
        ...

    @abstractmethod
    def delete(self, db: MySQLConnection, *, id: int) -> None:
        ...
