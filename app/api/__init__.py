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
