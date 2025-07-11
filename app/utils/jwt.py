from jose import jwt, JWTError
from app.schemas.token import TokenInfo
from app.utils.datetime import Datetime
import traceback

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_token(token_info: TokenInfo, token_ttl: int = 7200):
    token_info = token_info.model_copy(update={
        # "iss": '', # TODO
        # "aud": '', # TODO
        # "jti": '', # TODO
        # "iat": Datetime.now_timestamp(),
        # "nbf": Datetime.now_timestamp() - 30,
        "exp": Datetime.now_timestamp() + token_ttl,
    })
    return jwt.encode(dict(token_info), SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        print('decode_token', 'error', e)
        traceback.print_exc()
        return None
