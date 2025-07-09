from app.repos.user_repo import UserRepo

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def list_users(self):
        return await self.user_repo.get_all()
