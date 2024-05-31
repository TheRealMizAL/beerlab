from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.transactions import in_transaction

from core.schemas.security import Token
from core.db.models import Creds, User
from core.security import verify_passwd, create_access_token

oauth_router = APIRouter(prefix='/oauth2')


@oauth_router.post('/token')
async def get_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    not_auth_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"}
    )
    async with in_transaction() as connection:
        if user := await User.get_or_none(username=form_data.username, using_db=connection):
            await user.fetch_related('creds', using_db=connection)
            if not await verify_passwd(form_data.password, user.creds.passwd):
                raise not_auth_exeption
            access_token = await create_access_token({"first_name": user.first_name,
                                                      "last_name": user.last_name,
                                                      "sub": user.username,
                                                      "link": user.link})
            return Token(access_token=access_token, token_type="bearer")
        raise not_auth_exeption
