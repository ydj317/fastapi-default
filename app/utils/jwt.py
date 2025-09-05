from jose import jwt, JWTError
from app.schemas.token import TokenInfo
from app.utils.datetime import Datetime
from app.core.settings import settings
import traceback
import uuid

JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ALGORITHM = settings.jwt_algorithm
JWT_ISSUER = settings.jwt_issuer
JWT_AUDIENCE = settings.jwt_audience

def create_token(token_info: TokenInfo, token_ttl: int = 7200):
    token_info = token_info.model_copy(update={
        "iss": JWT_ISSUER,
        "aud": JWT_AUDIENCE,
        "jti": uuid.uuid4().hex,
        "iat": Datetime.now_timestamp(),
        "nbf": Datetime.now_timestamp() - 30,
        "exp": Datetime.now_timestamp() + token_ttl,
    })
    return jwt.encode(dict(token_info), JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], audience=JWT_AUDIENCE, issuer=JWT_ISSUER)
        return payload
    except JWTError as e:
        print('decode_token', 'error', e)
        traceback.print_exc()
        return None
