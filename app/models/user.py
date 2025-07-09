from pydantic import BaseModel

class UserJoin(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
