import json
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.core.containers import Container
from app.models.response import Res
from app.core.auth import get_token_info, TokenInfo
from app.utils.logs import Logs
from app.models.user import UserRead, JoinRequest, LoginRequest

router = APIRouter()

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

@router.post("/api/user/login", response_model=Res)
@inject
async def user_login(
        login_request: LoginRequest,
        user_service: UserService = Depends(Provide[Container.user_service])
):
    result = await user_service.login_user(username=login_request.username, password=login_request.password)
    return Res(data=result)

@router.get("/api/user/info", response_model=Res[TokenInfo])
async def user_login(token_info: TokenInfo = Depends(get_token_info)):
    return Res(data=token_info)

@router.get("/api/user", response_model=Res[list[UserRead]])
@inject
async def get_users(
    service: UserService = Depends(Provide[Container.user_service])
):
    user_list = await service.list_users()
    await Logs.info('user_list', json.dumps(user_list))
    return Res(data=user_list)