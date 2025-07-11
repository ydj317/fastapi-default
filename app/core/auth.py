from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from app.exceptions.PageAuthException import PageAuthException
from app.utils.jwt import decode_token
from app.schemas.token import TokenInfo
import traceback

"""
Authorization: Bearer <token>
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

async def get_token_info(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenInfo(**payload)

async def get_token_by_cookie(request: Request):
    try:
        token = request.cookies.get("token")
        payload = decode_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return TokenInfo(**payload)
    except Exception as e:
        print('get_token_by_cookie', 'error', e)
        traceback.print_exc()
        raise PageAuthException('authentication failed')

