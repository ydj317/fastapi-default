from app.models.user import UserRead
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.containers import Container
from app.tasks.user_task import send_welcome_email
from app.models.response import Res
from typing import List

router = APIRouter()

@router.get("/api/user", response_model=Res[List[UserRead]])
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    user_list = await service.list_users()
    return Res(data=user_list)

@router.get("/api/user/welcome-email")
def trigger_email():
    send_welcome_email.delay(2)
    return {"message": "Email will be sent in background."}