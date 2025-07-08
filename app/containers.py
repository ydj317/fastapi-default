from dependency_injector import containers, providers
from app.core.settings import settings
from app.db.database import database
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.redis import get_redis

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    config = providers.Configuration()
    config.database_url.from_value(settings.database_url)
    config.redis_url.from_value(settings.redis_url)
    config.rabbitmq_url.from_value(settings.rabbitmq_url)

    redis = providers.Resource(get_redis, url=config.redis_url)

    db = providers.Singleton(lambda: database)

    user_repository = providers.Factory(UserRepository, db=db)
    user_service = providers.Factory(UserService, repo=user_repository)
