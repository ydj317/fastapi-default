from dependency_injector import containers, providers
from app.core.settings import settings
from app.db.session import create_engine_pool, get_session_factory, get_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    config = providers.Configuration()
    config.database_url.from_value(settings.database_url)

    engine = providers.Singleton(create_engine_pool, db_url=config.database_url)
    session_factory = providers.Singleton(get_session_factory, engine=engine)
    db_session = providers.Resource(get_session, factory=session_factory)

    user_repository = providers.Factory(UserRepository, session=db_session)
    user_service = providers.Factory(UserService, repo=user_repository)
