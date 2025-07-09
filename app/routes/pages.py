from fastapi import APIRouter, Depends

from app.utils.template import Template

router = APIRouter()

@router.get("/pages")
def get_main(template: Template = Depends()):
    return template.response('index.html', {"name": "Jinja2"})
