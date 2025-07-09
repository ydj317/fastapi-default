from fastapi import APIRouter, Depends

from app.core.auth import get_token_by_cookie
from app.models.token import TokenInfo
from app.utils.template import Template

router = APIRouter()

@router.get("/pages")
def get_main(template: Template = Depends(), token_info: TokenInfo = Depends(get_token_by_cookie)):
    print(token_info)
    return template.response('index.html', {"name": "Jinja2"})
