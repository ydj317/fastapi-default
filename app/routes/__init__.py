from fastapi import APIRouter
from .api import router as api_router
from .main import router as main_router
from .user import router as user_router
from .test import router as test_router

router = APIRouter()

router.include_router(api_router)
router.include_router(main_router)
router.include_router(user_router)
router.include_router(test_router)
