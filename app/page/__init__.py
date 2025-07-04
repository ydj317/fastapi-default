from fastapi import APIRouter
from .routes.main import router as main_router
from .routes.users import router as user_router

router = APIRouter()
router.include_router(main_router)
router.include_router(user_router, prefix="/users")
