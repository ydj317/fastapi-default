from fastapi import APIRouter
from .routes.users import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/users")