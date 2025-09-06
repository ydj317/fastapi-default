from fastapi import APIRouter
from .api import router as api_router
from .page import router as page_router
from .test import router as test_router

router = APIRouter()

router.include_router(api_router)
router.include_router(page_router)
router.include_router(test_router)
