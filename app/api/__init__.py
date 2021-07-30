from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from app.api import deps

from app.api.routes import user
from app import crud, schemas

router = APIRouter()
router.include_router(user.router, prefix="/user")


@router.post("/user/")
def create_new_user(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserCreate
) -> schemas.UserCreate:
    data = crud.user.create(
        db, data=schemas.UserCreate(email=data.email, password=data.password)
    )
    return data


@router.put("/user/")
def update_user_data(
    data: schemas.UserUpdate,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.UserUpdate:
    crud.user.update(db, id=current_user.id, data=data)
    return schemas.Msg(msg="User was successfully updated")
