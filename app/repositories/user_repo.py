from databases import Database
import sqlalchemy

metadata = sqlalchemy.MetaData()

t_user = sqlalchemy.Table(
    "t_user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(length=50)),
    sqlalchemy.Column("password", sqlalchemy.String(length=32)),
)

class UserRepo:
    def __init__(self, db: Database):
        self.db = db

    async def create_user(self, username: str, password: str):
        query = t_user.insert().values(username=username, password=password)
        return await self.db.execute(query)

    async def get_all(self):
        query = t_user.select()
        users = await self.db.fetch_all(query)
        return [dict(user) for user in users]
