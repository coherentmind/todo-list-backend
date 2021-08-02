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
) -> schemas.UserReturn:
    res = crud.user.create(
        db, data=schemas.UserCreate(email=data.email, password=data.password)
    )
    return res


@router.put("/user/")
def update_user_data(
    data: schemas.UserUpdate,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.UserUpdate:
    crud.user.update(db, id=current_user.id, data=data)
    return schemas.Msg(msg="User was successfully updated")


@router.post("/task/")
def create_new_task(
    data: schemas.TaskCreateExtended,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.TaskCreate:
    data_extended = schemas.TaskCreateExtended(**data.dict(), owner_id=current_user.id)
    crud.task.create(db, data=data_extended)
    return schemas.TaskReturn


@router.put("/task/")
def update_task_data(
    data: schemas.TaskUpdate,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.TaskUpdate:
    crud.task.update(db, id=current_user, data=data)
    return schemas.Msg(msg="Task was seccessfully updated")


@router.delete("/task/")
def delete_task(
    data: schemas.TaskReturn,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> None:
    crud.task.delete(db, id=data.id)
    return schemas.Msg(msg="Your task was seccessfully deleted")