from jinja2 import Environment, FileSystemLoader
from pathlib import Path

BASE_DIR = Path(__file__).parent / "queries"
env = Environment(loader=FileSystemLoader(BASE_DIR))

def render_sql(path: str, context: dict) -> str:
    template = env.get_template(path)
    return template.render(context)
