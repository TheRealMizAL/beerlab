from datetime import timedelta, datetime, timezone
from typing import Optional, Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from core.schemas.security import TokenData
from core.settings import get_settings, get_rsa_public, get_rsa_private

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth2/token")


async def verify_passwd(plain, hashed):
    return pwd_context.verify(plain, hashed)


async def get_passwd_hash(passwd):
    return pwd_context.hash(passwd)


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(get_settings().access_token_exp_mins)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_rsa_private(), algorithm=get_settings().jws_alg)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, get_rsa_public(), algorithms=get_settings().jws_alg)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(**payload)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
