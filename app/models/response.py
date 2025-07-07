from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Res(BaseModel, Generic[T]):
    success: bool = True
    message: str = "성공"
    data: Optional[T] = None
