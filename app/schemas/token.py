from pydantic import BaseModel
from typing import Optional

class TokenInfo(BaseModel):
    sub: str
    exp: Optional[int] = None
