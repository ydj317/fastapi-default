from app.core.containers import Container
from app.consumers.stream import stream_app
from app.core.settings import settings

"""
실행 방법
faststream run app.worker:stream_app
"""

container = Container()
container.config.from_dict(settings.dict())

async def on_startup():
    await container.init_resources()

async def on_shutdown():
    await container.shutdown_resources()

stream_app.on_startup(on_startup)
stream_app.on_shutdown(on_shutdown)

