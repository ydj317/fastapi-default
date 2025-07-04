from fastapi import Depends
from app.db.session import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.query_loader import render_sql
from app.models.user import UserCreate

class UserService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_user(self, user: UserCreate):
        sql = "INSERT INTO users (name, email) VALUES (:name, :email)"
        await self.session.execute(text(sql), {"name": user.name, "email": user.email})
        await self.session.commit()

    async def get_user_by_id(self, user_id: int):
        sql = render_sql("user/get_user_by_id.sql", {"id": user_id})
        result = await self.session.execute(text(sql), {"id": user_id})
        row = result.fetchone()
        return row if row else None

    async def search_users(self, name: str = None, email: str = None, limit=10, offset=0):
        sql = render_sql("user/search_users.sql", {
            "name": name,
            "email": email,
            "limit": limit,
            "offset": offset
        })
        params = {
            "name": f"%{name}%" if name else None,
            "email": f"%{email}%" if email else None,
            "limit": limit,
            "offset": offset
        }
        result = await self.session.execute(text(sql), params)
        return [row for row in result.fetchall()]
