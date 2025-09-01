from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.context import get_is_login, get_username
from fastapi.responses import HTMLResponse
from jinja2 import select_autoescape
from jinja2_async_environment.environment import AsyncEnvironment
from jinja2_async_environment.loaders import AsyncFileSystemLoader

class Template:
    def __init__(self, request: Request):
        self.request = request

    async def bind_globals(self, env: AsyncEnvironment):
        container = self.request.app.container
        services = {
            "user": container.user_service,
        }

        async def service(service_name: str):
            return await services[service_name]()

        env.globals["service"] = service


    async def response(self, template_name: str, template_data = None):
        if template_data is None:
            template_data = {}

        env = AsyncEnvironment(
            loader=AsyncFileSystemLoader("app/templates"),
            autoescape=select_autoescape(["html", "xml"]),
            enable_async=True
        )

        await self.bind_globals(env)

        query = self.request.query_params
        context = {
            "request": self.request,
            "query": query,
            "is_login": get_is_login(),
            "username": get_username(),
            **template_data
        }

        template = await env.get_template_async(template_name)
        content = await template.render_async(**context)

        return HTMLResponse(content=content)


class TemplateSync:
    def __init__(self, request: Request):
        self.request = request
        self.template = Jinja2Templates(directory="app/templates")

    def response(self, template_name: str, template_data = None):
        if template_data is None:
            template_data = {}
        query = self.request.query_params
        context = {
            "request": self.request,
            "query": query,
            "is_login": get_is_login(),
            "username": get_username(),
            **template_data
        }
        return self.template.TemplateResponse(template_name, context)
