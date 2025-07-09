import json

from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.core.containers import Container
from app.models.response import Res
from pydantic import BaseModel
from app.utils.jwt import create_token
from datetime import timedelta
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
        user_repo: UserRepo = Depends(Provide[Container.user_repo])
):
    print(join_request)
    user_id = await user_repo.create(username=join_request.username, password=join_request.password)
    return Res(data={"user_id": user_id})


class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/user/login", response_model=Res)
async def user_login(login_request: LoginRequest):
    print(login_request)
    user = {"sub": login_request.username, **dict(login_request)}
    token = create_token(user, timedelta(minutes=120))
    return Res(data={"token": token})


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