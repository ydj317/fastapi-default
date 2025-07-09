from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.core.middleware import register_middleware
from app.core.exception import register_exception_handlers
from app.core.router import register_routers

app = FastAPI(lifespan=lifespan)

register_middleware(app)
register_exception_handlers(app)
register_routers(app)
