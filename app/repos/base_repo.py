from abc import ABC, abstractmethod
from databases import Database
import sqlalchemy
from datetime import datetime

class BaseRepo(ABC):
    def __init__(self, db: Database):
        self.db = db

    @property
    @abstractmethod
    def table(self) -> sqlalchemy.Table:
        """서브클래스가 구현해야 할 SQLAlchemy Table"""
        pass

    def _has_column(self, column_name: str) -> bool:
        return column_name in self.table.c

    def _now(self):
        return datetime.now()

    async def create(self, **values):
        if self._has_column("created_at") and "created_at" not in values:
            values["created_at"] = self._now()
        query = self.table.insert().values(**values)
        return await self.db.execute(query)

    async def get_all(self):
        query = self.table.select()
        rows = await self.db.fetch_all(query)
        return [dict(row) for row in rows]

    async def get_by_id(self, id: int):
        query = self.table.select().where(self.table.c.id == id)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None

    async def update_by_id(self, id: int, **values):
        if self._has_column("updated_at"):
            values["updated_at"] = self._now()
        query = self.table.update().where(self.table.c.id == id).values(**values)
        return await self.db.execute(query)

    async def delete_by_id(self, id: int):
        query = self.table.delete().where(self.table.c.id == id)
        return await self.db.execute(query)
