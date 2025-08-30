from fastapi import APIRouter, Depends, Request
from app.utils.template import Template
from dependency_injector.wiring import inject, Provide
from app.services.user_service import UserService
from app.core.containers import Container

router = APIRouter()


@router.get("/")
def main_page(template: Template = Depends()):
    return template.response('index.html')


@router.get("/user/login")
def login_page(template: Template = Depends()):
    return template.response('user/login.html')


@router.get("/user/logout")
def login_page(request: Request, template: Template = Depends()):
    response = template.response('user/logout.html')
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
    return template.response(
        'user/info.html',
        {
            'user': await user_service.current_user()
        }
    )
