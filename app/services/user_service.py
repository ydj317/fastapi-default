from app.exceptions.SystemException import SystemException
from app.repos.user_info_repo import UserInfoRepo
from app.repos.user_repo import UserRepo
from app.schemas.user import JoinRequest
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_token
from app.schemas.token import TokenInfo
from app.core.context import get_username

class UserService:
    def __init__(self, user_repo: UserRepo, user_info_repo: UserInfoRepo):
        self.user_repo = user_repo
        self.user_info_repo = user_info_repo

    async def current_user(self):
        user = await self.user_repo.get_by_username(get_username())
        if user is None:
            return {}
        user_info = await self.user_info_repo.get_by_user_id(user["id"])
        user_info.pop("id", None)
        return user | user_info

    async def join_user(self, join_request: JoinRequest):
        user = await self.user_repo.get_by_username(join_request.username)
        if user is not None:
            raise SystemException('duplicate username')
        return await self.user_repo.create(**join_request.model_dump())

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
