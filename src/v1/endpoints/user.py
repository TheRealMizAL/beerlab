from typing import Annotated

from fastapi import APIRouter, Path, Response, HTTPException, status
from tortoise.transactions import in_transaction

from core.db.models import User, Creds
from core.schemas.user import UserFullModel, UserMinModel, UserRegisterModel
from core.schemas.errors import BadUserError

user_router = APIRouter(prefix='/user',
                        tags=['User'])


@user_router.get('/{user_id}',
                 responses={200: {'model': UserFullModel},
                            404: {'model': BadUserError}})
async def get_user(user_id: Annotated[int, Path()]) -> UserFullModel:
    async with in_transaction() as connection:
        if user := await User.get_or_none(id=user_id, using_db=connection):
            return user
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadUserError)


@user_router.post('/', status_code=status.HTTP_201_CREATED)
async def register_user(response: Response, user: UserRegisterModel) -> UserFullModel:
    async with in_transaction() as connection:
        user = user.dict(exclude_unset=True)
        user_db = await User.create(**user, using_db=connection)
        await Creds(user_id=user_db.id, login=user['login'], passwd=user['password']).save(using_db=connection)
    response.status_code = status.HTTP_201_CREATED
    return user_db


@user_router.put('/{user_id}',
                 responses={200: {'model': UserFullModel},
                            201: {'model': UserFullModel}})
async def change_user(response: Response, user_id: Annotated[int, Path()], user: UserMinModel):
    async with in_transaction() as connection:
        user_created = await User.update_or_create(defaults=user.dict(), id=user_id, using_db=connection)
        if user_created[1]:
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_200_OK
        return user_created[0]


@user_router.patch('/{user_id}',
                   responses={200: {'model': UserFullModel},
                              404: {'model': BadUserError}})
async def edit_user(response: Response, user_id: Annotated[int, Path()], user: UserMinModel):
    async with in_transaction() as connection:
        if user_db := await User.get_or_none(id=user_id, using_db=connection):
            await user_db.update_from_dict(user.dict(exclude_unset=True))
            await user_db.save(using_db=connection)
            response.status_code = status.HTTP_200_OK
            return user_db
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadUserError)


@user_router.delete('/{user_id}',
                    responses={204: {'model': None},
                               404: {'model': BadUserError}})
async def delete_user(response: Response, user_id: Annotated[int, Path()]):
    async with in_transaction() as connection:
        if user := await User.get_or_none(id=user_id, using_db=connection):
            await user.delete(using_db=connection)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadUserError)
