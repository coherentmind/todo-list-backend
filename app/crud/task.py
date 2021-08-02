from mysql.connector import cursor
from mysql.connector.cursor import CursorBase
from pydantic.errors import EmailError
from app.crud.base import BaseCRUD
from typing import Optional
from app import schemas
from mysql.connector import MySQLConnection


class TaskCRUD(
    BaseCRUD[schemas.TaskCreateExtended, schemas.TaskUpdate, schemas.TaskReturn]
):
    def get(self, db: MySQLConnection, *, id: int) -> Optional[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id, name, completness, date FROM task WHERE id={id}")
        try:
            data = next(cursor)
        except StopIteration:
            return None
        else:
            id = data
            return schemas.TaskReturn(id=id)
        finally:
            cursor.close()

    def get_multi(self, db: MySQLConnection) -> list[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(f"SELECT id FROM task")
        res = [schemas.TaskReturn(id=id) for id in cursor]
        cursor.close()
        return res

    def get_multi_by_owner(
        self, db: MySQLConnection, *, owner_id: int
    ) -> list[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(f"SELECT name FROM task WHERE owner_id='{id}'")
        res = [schemas.TaskReturn(id=id) for id in cursor]
        cursor.close()
        return res

    def create(
        self, db: MySQLConnection, *, data: schemas.TaskCreateExtended
    ) -> schemas.TaskReturn:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO task (id, name, completness, date) VALUES('{data.name}', '{data.completness}')"
        )
        cursor.execute(f"SELECT LAST_INSERT_ID()")
        (id,) = next(cursor)
        db.commit()
        cursor.close()
        return self.get(db, id=id)

    def update(self, db: MySQLConnection, *, data: schemas.TaskUpdate) -> None:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE task SET name='{data.name}', completness='{data.completness}' WHERE id='{id}'"
        )
        db.commit()
        cursor.close()
        return None

    def delete(self, db: MySQLConnection, *, id: int) -> None:
        cursor = db.cursor()
        if id not in cursor.execute(f"SELECT * FROM users WHERE id='{id}'"):
            cursor.close()
            return None