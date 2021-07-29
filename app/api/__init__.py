from fastapi import APIRouter, Depends
from mysql.connector import MySQLConnection
from app.api import deps

from app.api.routes import user
from app import crud, schemas

router = APIRouter()
router.include_router(user.router, prefix="/user")


@router.get("/")
async def root(db: MySQLConnection = Depends(deps.get_db)):
    data = crud.user.create(db, data=schemas.UserCreate(email="test", password="test"))
    return {"message": data}


@router.post("/")
def create_new_user(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserCreate = Depends()
) -> schemas.UserCreate:
    data = crud.user.create(
        db, data=schemas.UserCreate(email=data.email, password=data.password)
    )
    return data


@router.put("/")
def update_user_data(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserUpdate = Depends()
) -> schemas.UserUpdate:
    data = crud.user.update(db, data=schemas.UserUpdate(password=data.password))
    return schemas.Msg(msg="User was successfully updated")


@router.delete("/")
def delete_user(
    db: MySQLConnection = Depends(deps.get_db), *, data: schemas.UserReturn = Depends()
) -> schemas.UserReturn:
    crud.user.delete(db, data=schemas.UserUpdate(id=str(data.id)))
    return schemas.Msg(msg="User was successfully deleted")