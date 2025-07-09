from fastapi import FastAPI
from app.routes import router
from fastapi.staticfiles import StaticFiles

def register_routers(app: FastAPI):
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")