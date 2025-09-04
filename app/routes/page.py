from fastapi import APIRouter, Depends
from app.utils.template import Template

router = APIRouter()

@router.get("/")
async def main_page(template: Template = Depends()):
    return await template.response('index.html')

