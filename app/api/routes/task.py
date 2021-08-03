from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from app.api import deps
from fastapi import HTTPException
from app import schemas, crud

router = APIRouter()


@router.get("/")
def get_tasks_of_user(
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> list[schemas.TaskReturn]:
    return crud.task.get_multi_by_owner(db, owner_id=current_user.id)


@router.post("/")
def create_new_task(
    data: schemas.TaskCreate,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.TaskReturn:
    data_extended = schemas.TaskCreateExtended(**data.dict(), owner_id=current_user.id)
    res = crud.task.create(db, data=data_extended)
    return res


@router.put("/")
def update_task_data(
    data: schemas.TaskUpdate,
    task_id: int,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.Msg:
    get_request = crud.task.get(db, id=task_id)
    if not get_request:
        raise HTTPException(404, "Not found")
    elif current_user.id != get_request.owner_id:
        raise HTTPException(403, "Forbidden")
    else:
        crud.task.update(db, id=task_id, data=data)
        return schemas.Msg(msg="Task was successfully updated")


@router.delete("/")
def delete_task(
    task_id: int,
    db: MySQLConnection = Depends(deps.get_db),
    current_user: schemas.UserReturn = Depends(deps.get_current_user),
) -> schemas.Msg:
    get_request = crud.task.get(db, id=task_id)
    if not get_request:
        raise HTTPException(404, "Not found")
    elif current_user.id != get_request.owner_id:
        raise HTTPException(403, "Forbidden")
    else:
        crud.task.delete(db, id=task_id)
        return schemas.Msg(msg="Your task was seccessfully deleted")