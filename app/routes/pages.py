from fastapi import APIRouter, Depends, Request
from app.utils.template import Template
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.core.containers import Container
from app.utils.logs import Logs

router = APIRouter()


@router.get("/")
async def main_page(template: Template = Depends()):
    return await template.response('index.html')


@router.get("/user/login")
async def login_page(template: Template = Depends()):
    return await template.response('user/login.html')


@router.get("/user/logout")
async def login_page(request: Request, template: Template = Depends()):
    response = await template.response('user/logout.html')
    for cookie_name in request.cookies.keys():
        response.delete_cookie(cookie_name)
    return response


@router.get("/user/info")
@inject
async def pages(
        template: Template = Depends(),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    print(await user_service.current_user())
    await Logs.info(message="dfdsfdsfsdf", data="fdsfsd")
    return await template.response(
        'user/info.html',
        {
            'user': await user_service.current_user(),
            'user_service': user_service,
        }
    )
