from app.exceptions.SystemException import SystemException
from app.repos.user_repo import UserRepo
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_token
from app.schemas.token import TokenInfo

class UserService:
    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def join_user(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if user is not None:
            raise SystemException('duplicate username')
        return await self.user_repo.create(username=username, password=hash_password(password))

    async def login_user(self, username: str, password: str):
        user = await self.user_repo.get_by_username(username)
        if user is None:
            raise SystemException('invalid username')
        if not verify_password(password, user['password']):
            raise SystemException('invalid password')
        token_info = TokenInfo(sub=user['username'])
        token = create_token(token_info, 7200)
        return {"token": token}

    async def list_users(self):
        return await self.user_repo.get_all()
