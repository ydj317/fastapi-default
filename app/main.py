from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.page import router as page_router
from app.api import router as api_router

app = FastAPI()

app.include_router(page_router)
app.include_router(api_router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

