from databases import Database

class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_all(self):
        result = await self.db.fetch_all("SELECT * FROM users")
        return result
