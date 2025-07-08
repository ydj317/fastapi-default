from app.models.user import UserRead
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.containers import Container
from app.models.response import Res
from typing import List
from pydantic import BaseModel
from app.auth.jwt import create_access_token
from datetime import timedelta
from app.auth.dependencies import get_token_info

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/user/login", response_model=Res)
async def user_login(login_request: LoginRequest):
    print(login_request)
    user = {"sub": login_request.username, **dict(login_request)}
    token = create_access_token(user, timedelta(minutes=5))
    return Res(data={"token": token})


@router.get("/api/user/info", response_model=Res)
async def user_login(token_info = Depends(get_token_info)):
    return Res(data=token_info)

@router.get("/api/user", response_model=Res[List[UserRead]])
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    user_list = await service.list_users()
    return Res(data=user_list)