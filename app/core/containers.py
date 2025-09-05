from dependency_injector import containers, providers
from app.core.database import get_database
from app.repos.logs_repo import LogsRepo
from app.repos.user_repo import UserRepo
from app.services.user_service import UserService
from app.core.redis import get_redis
from app.utils.logs import Logs



async def init_logs(logs_repo: LogsRepo):
    Logs.init(logs_repo=logs_repo)
    print("✅ Logs initialized")
    try:
        yield
    finally:
        pass

class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    config = providers.Configuration()

    redis = providers.Resource(
        get_redis,
        url=config.redis_url
    )

    db = providers.Resource(
        get_database,
        database_url=config.database_url,
        min_size=config.database_pool_min_size,
        max_size=config.database_pool_max_size,
    )

    logs_repo = providers.Singleton(LogsRepo, db=db)

    # init_resources() 호출 시 자동 실행되는 Resource
    logs_init = providers.Resource(init_logs, logs_repo=logs_repo)

    user_repo = providers.Factory(UserRepo, db=db)
    user_service = providers.Factory(UserService, user_repo=user_repo)


