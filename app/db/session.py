from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

def create_engine_pool(db_url: str):
    return create_async_engine(
        db_url,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_recycle=1800,
        pool_pre_ping=True
    )

def get_session_factory(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_session(factory) -> AsyncSession:
    async with factory() as session:
        yield session
