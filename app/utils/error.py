from urllib.request import Request

from app.utils.template import Template


async def error401(request: Request):
    template = Template(request)
    response = await template.response('error/401.html')
    response.status_code = 401
    return response

async def error404(request: Request):
    template = Template(request)
    response = await template.response('error/404.html')
    response.status_code = 404
    return response

async def error500(request: Request):
    template = Template(request)
    response = await template.response('error/500.html')
    response.status_code = 500
    return response