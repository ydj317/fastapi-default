from dependency_injector import containers, providers
from app.core.settings import settings
from app.core.database import database
from app.repos.logs_repo import LogsRepo
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.core.redis import get_redis

async def get_database():
    await database.connect()
    print("✅ Database connected")
    try:
        yield database
    finally:
        await database.disconnect()
        print("🔌 Database disconnected")

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    config = providers.Configuration()
    config.database_url.from_value(settings.database_url)
    config.redis_url.from_value(settings.redis_url)
    config.rabbitmq_url.from_value(settings.rabbitmq_url)

    redis = providers.Resource(get_redis, url=config.redis_url)

    db = providers.Resource(get_database)

    logs_repo = providers.Singleton(LogsRepo, db=db)

    user_repo = providers.Factory(UserRepo, db=db)
    user_service = providers.Factory(UserService, user_repo=user_repo)
