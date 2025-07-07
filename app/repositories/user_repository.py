from databases import Database

class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self):
        users = await self.db.fetch_all("SELECT * FROM users")
        return [dict(user) for user in users]
