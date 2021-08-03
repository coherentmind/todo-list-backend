from fastapi import APIRouter
from app.api.routes import user, task


router = APIRouter()
router.include_router(user.router, prefix="/user")
router.include_router(task.router, prefix="/task")
