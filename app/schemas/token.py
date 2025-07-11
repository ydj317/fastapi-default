from pydantic import BaseModel
from typing import Optional

class TokenInfo(BaseModel):
    # iss: Optional[str] = None # 토큰을 발행한 주체 (예: 서비스 이름, 도메인 등)
    # aud: Optional[str] = None # 이 토큰을 사용할 수 있는 대상 (예: 클라이언트 ID 등)
    sub: str # 토큰의 주제, 보통 사용자 ID 또는 고유 식별자
    # jti: Optional[str] = None # 토큰의 고유 식별자 (중복 방지 또는 토큰 무효화에 사용)
    # iat: Optional[int] = None # 토큰이 발급된 시간 (Unix timestamp)
    # nbf: Optional[int] = None # 이 시간 전에는 토큰이 유효하지 않음 (Unix timestamp)
    exp: Optional[int] = None # 토큰의 만료 시간 (Unix timestamp)
