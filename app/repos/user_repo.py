import sqlalchemy

from app.repos.base_repo import BaseRepo

table = sqlalchemy.Table(
    "t_user",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(50)),
    sqlalchemy.Column("password", sqlalchemy.String(200)),
)

class UserRepo(BaseRepo):
    @property
    def table(self):
        return table

    async def get_by_username(self, username: str):
        query = self.table.select().where(self.table.c.username == username)
        row = await self.db.fetch_one(query)
        return dict(row) if row else None
