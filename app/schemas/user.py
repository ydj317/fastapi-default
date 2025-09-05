from pydantic import BaseModel

class JoinRequest(BaseModel):
    username: str
    password: str
    nickname: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    nickname: str