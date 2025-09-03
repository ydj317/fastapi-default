from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.context import get_is_login, get_username
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("app/templates"),
    autoescape=select_autoescape(["html", "xml"]),
    enable_async=True
)

class Template:
    def __init__(self, request: Request):
        self.request = request

    async def bind_globals(self):
        container = self.request.app.container
        async def service(service_name: str):
            return await getattr(container, service_name)()

        env.globals["container"] = service

    async def response(self, template_name: str, template_data = None):
        if template_data is None:
            template_data = {}

        await self.bind_globals()

        query = self.request.query_params
        context = {
            "request": self.request,
            "query": query,
            "is_login": get_is_login(),
            "username": get_username(),
            **template_data
        }

        template = env.get_template(template_name)
        content = await template.render_async(**context)

        return HTMLResponse(content=content)
