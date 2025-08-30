from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from app.core.context import get_is_login, get_username

class Template:
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


