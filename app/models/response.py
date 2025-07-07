from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class Res(GenericModel, Generic[T]):
    success: bool = True
    message: str = "성공"
    data: Optional[T] = None
