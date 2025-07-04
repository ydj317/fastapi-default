from fastapi import Request
from fastapi.templating import Jinja2Templates

class Template:
    def __init__(self, request: Request):
        self.request = request
        self.template = Jinja2Templates(directory="app/templates")

    def response(self, template_name: str, template_data: dict):
        query = self.request.query_params
        context = {"request": self.request, "query": query, **template_data}
        return self.template.TemplateResponse(template_name, context)


