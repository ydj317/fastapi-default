from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(text("SELECT * FROM users"))
        return [dict(row._mapping) for row in result.fetchall()]
