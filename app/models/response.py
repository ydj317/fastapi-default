from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Res(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: Optional[T] = None
