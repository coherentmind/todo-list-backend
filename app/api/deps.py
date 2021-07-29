from app import db
from typing import Optional
from mysql.connector import MySQLConnection
from fastapi import Depends, HTTPException
from app import schemas
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def get_db() -> MySQLConnection:
    connection = db.connect()
    try:
        yield connection
    finally:
        connection.close()


security = HTTPBasic()


def get_current_user(
    db: MySQLConnection = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(security),
) -> schemas.UserReturn:
    cursor = db.cursor()
    cursor.execute(
        f"SELECT id, email FROM users WHERE email='{credentials.username}' AND password='{credentials.password}'"
    )
    try:
        data = next(cursor)
    except StopIteration:
        raise HTTPException(401, detail="Incorrect email or password")
    else:
        id, email = data
        return schemas.UserReturn(id=id, email=email)
    finally:
        cursor.close()
