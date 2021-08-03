from app import crud, db, schemas
from fastapi import APIRouter, HTTPException
from typing import Any, Union
from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from app.api import deps

router = APIRouter()


@router.post("/")
def create_new_user(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserCreate
) -> schemas.UserReturn:
    res = crud.user.create(
        db, data=schemas.UserCreate(email=data.email, password=data.password)
    )
    return res


@router.put("/")
def update_user_data(
    data: schemas.UserUpdate,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.UserUpdate:
    crud.user.update(db, id=current_user.id, data=data)
    return schemas.Msg(msg="User was successfully updated")