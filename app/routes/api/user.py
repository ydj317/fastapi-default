import json

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.core.containers import Container
from app.models.response import Res
from pydantic import BaseModel
from app.core.auth import get_token_info
from app.utils.logs import Logs

router = APIRouter()

class JoinRequest(BaseModel):
    username: str
    password: str

@router.post("/api/user/join", response_model=Res)
@inject
async def user_join(
        join_request: JoinRequest,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    print(join_request)
    result = await user_service.join_user(join_request.username, join_request.password)
    print(result)
    return Res()


class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/user/login", response_model=Res)
@inject
async def user_login(
        login_request: LoginRequest,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    result = await user_service.login_user(username=login_request.username, password=login_request.password)
    return Res(data=result)


@router.get("/api/user/info", response_model=Res)
async def user_login(token_info = Depends(get_token_info)):
    return Res(data=token_info)

class UserRead(BaseModel):
    id: int
    username: str

@router.get("/api/user", response_model=Res[list[UserRead]])
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    user_list = await service.list_users()
    await Logs.info('user_list', json.dumps(user_list))
    return Res(data=user_list)