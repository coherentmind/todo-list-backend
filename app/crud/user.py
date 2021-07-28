from mysql.connector import cursor
from mysql.connector.cursor import CursorBase
from app.crud.base import BaseCRUD
from typing import Any, Optional
from app import schemas
from mysql.connector import MySQLConnection


class UserCRUD(BaseCRUD[schemas.UserCreate, schemas.UserUpdate, schemas.UserReturn]):
    def get(self, db: MySQLConnection, *, id: int) -> Optional[schemas.UserReturn]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id, email FROM users WHERE id={id}")
        try:
            data = next(cursor)
        except StopIteration:
            return None
        else:
            id, email = data
            return schemas.UserReturn(id=id, email=email)
        finally:
            cursor.close()

    def get_multi(self, db: MySQLConnection) -> list[schemas.UserReturn]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id, email FROM users")
        res = [schemas.UserReturn(id=id, email=email) for (id, email) in cursor]
        cursor.close()
        return res

    def create(
        self, db: MySQLConnection, *, data: schemas.UserCreate
    ) -> schemas.UserReturn:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO users (email, password) VALUES('{data.email}', '{data.password}')"
        )
        cursor.execute(f"SELECT LAST_INSERT_ID()")
        (id,) = next(cursor)
        cursor.close()
        return self.get(db, id=id)

    def update(self, db: MySQLConnection, *, id: int, data: schemas.UserUpdate) -> None:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE users SET password='{data.password}' WHERE id='{data.id}'"
        )
        cursor.close()

    def delete(self, db: MySQLConnection, *, id: int) -> None:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM users WHERE id='{id}'")
        cursor.close()