from fastapi import APIRouter, Request, Depends

from app.utils.template import Template

router = APIRouter()

@router.get("/")
def get_main(template: Template = Depends()):
    return template.response('index.html', {"name": "Hello!!!"})
