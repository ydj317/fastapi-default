from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.utils.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

async def get_token_info(token: str = Depends(oauth2_scheme)):
    print(f"token: {token}")

    payload = decode_token(token)

    print(f"payload: {payload}")

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return payload
