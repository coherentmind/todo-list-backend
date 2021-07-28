from fastapi import APIRouter, Depends
from mysql.connector import Connector
from app.api import deps

from app.api.routes import user

router = APIRouter()
router.include_router(user.router, prefix="/user")


@router.get("/")
async def root(db: Connector = Depends(deps.get_db)):
    return {"message": "Hello World"}
