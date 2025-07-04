import os
from typing import AsyncGenerator, Callable, Any, Coroutine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession
)
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self._url = os.getenv("DATABASE_URL")
        if not self._url:
            raise RuntimeError("env.DATABASE_URL Not Defined!")

        self.engine: AsyncEngine = create_async_engine(
            self._url,
            echo=True,
            pool_size=5,
            max_overflow=10,
            pool_recycle=1800,
            pool_pre_ping=True,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def with_transaction(
        self,
        handler: Callable[[AsyncSession], Coroutine[Any, Any, Any]]
    ) -> Any:
        """
        트랜잭션 래핑 유틸:
        await db.with_transaction(lambda session: your_logic(session))
        """
        async with self.session_factory() as session:
            try:
                async with session.begin():
                    return await handler(session)
            except Exception:
                await session.rollback()
                raise

    async def connect(self) -> None:
        """FastAPI startup event 등에서 연결 체크용"""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(lambda conn: None)
            print("✅ DB 연결 성공")
        except OperationalError as e:
            raise RuntimeError(f"❌ DB 연결 실패: {e}")

    async def disconnect(self) -> None:
        await self.engine.dispose()
        print("🔌 DB 연결 종료")


# 싱글턴 인스턴스
db = Database()

# FastAPI 의존성 주입용
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db.get_session():
        yield session
