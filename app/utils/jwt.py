from jose import jwt, JWTError
from app.schemas.token import TokenInfo
from app.utils.datetime import Datetime
import traceback
import uuid

JWT_SECRET = "your-secret-key"
JWT_ALGORITHM = "HS512"
JWT_ISSUER = "system"
JWT_AUDIENCE = "app"

def create_token(token_info: TokenInfo, token_ttl: int = 7200):
    token_info = token_info.model_copy(update={
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": uuid.uuid4().hex,
        "iat": Datetime.now_timestamp(),
        "nbf": Datetime.now_timestamp() - 30,
        "exp": Datetime.now_timestamp() + token_ttl,
    })
    return jwt.encode(dict(token_info), JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
        return payload
    except JWTError as e:
        print('decode_token', 'error', e)
        traceback.print_exc()
        return None
