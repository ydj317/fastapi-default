from app.models.user import UserRead
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.containers import Container

router = APIRouter()

@router.get("/api/user", response_model=list[UserRead])
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    return await service.list_users()