from mysql.connector import cursor
from mysql.connector.cursor import CursorBase
from pydantic.errors import EmailError
from app.crud.base import BaseCRUD
from typing import Optional
from app import schemas
from mysql.connector import MySQLConnection
from datetime import datetime


class TaskCRUD(
    BaseCRUD[schemas.TaskCreateExtended, schemas.TaskUpdate, schemas.TaskReturn]
):
    def get(self, db: MySQLConnection, *, id: int) -> Optional[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, task_name, completeness, creation_date, owner_id FROM task WHERE id={id}"
        )
        try:
            data = next(cursor)
        except StopIteration:
            return None
        else:
            (id, task_name, completeness, creation_date, owner_id) = data
            return schemas.TaskReturn(
                id=id,
                task_name=task_name,
                completeness=completeness,
                creation_date=creation_date,
                owner_id=owner_id,
            )
        finally:
            cursor.close()

    def get_multi(self, db: MySQLConnection) -> list[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, task_name, completeness, creation_date, owner_id FROM task"
        )
        res = [
            schemas.TaskReturn(
                id=id,
                task_name=task_name,
                completeness=completeness,
                creation_date=creation_date,
                owner_id=owner_id,
            )
            for id, task_name, completeness, creation_date, owner_id in cursor
        ]
        cursor.close()
        return res

    def get_multi_by_owner(
        self, db: MySQLConnection, *, owner_id: int
    ) -> list[schemas.TaskReturn]:
        cursor = db.cursor()
        cursor.execute(
            f"SELECT id, task_name, completeness, creation_date, owner_id FROM task WHERE owner_id='{owner_id}'"
        )
        res = [
            schemas.TaskReturn(
                id=id,
                task_name=task_name,
                completeness=completeness,
                creation_date=creation_date,
                owner_id=owner_id,
            )
            for id, task_name, completeness, creation_date, owner_id in cursor
        ]
        cursor.close()
        return res

    def create(
        self, db: MySQLConnection, *, data: schemas.TaskCreateExtended
    ) -> schemas.TaskReturn:
        cursor = db.cursor()
        cursor.execute(
            f"INSERT INTO task (task_name, creation_date, owner_id) VALUES('{data.task_name}', '{datetime.now()}', '{data.owner_id}')"
        )
        cursor.execute(f"SELECT LAST_INSERT_ID()")
        (id,) = next(cursor)
        db.commit()
        cursor.close()
        return self.get(db, id=id)

    def update(self, db: MySQLConnection, *, data: schemas.TaskUpdate, id: int) -> None:
        cursor = db.cursor()
        cursor.execute(
            f"UPDATE task SET task_name='{data.task_name}', completness='{int(data.completness)}' WHERE id='{id}'"
        )
        db.commit()
        cursor.close()
        return None

    def delete(self, db: MySQLConnection, *, id: int) -> None:
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM task WHERE id='{id}'")
        db.commit()
        cursor.close()