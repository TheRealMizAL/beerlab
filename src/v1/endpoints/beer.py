from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, status, Response
from tortoise.transactions import in_transaction

from core.db.models import Beer
from core.schemas.beer import BeerFullModel, BeerMinModel
from core.schemas.errors import BadBeerError

beer_router = APIRouter(prefix='/beer',
                        tags=['Beer'])


@beer_router.get('/{beer_id}',
                 responses={200: {'model': BeerFullModel},
                            404: {'model': BadBeerError}})
async def get_beer(beer_id: Annotated[int, Path()]) -> BeerFullModel:
    async with in_transaction() as connection:
        if beer := await Beer.get_or_none(id=beer_id, using_db=connection):
            return beer
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadBeerError)


@beer_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_beer(response: Response, beer: BeerMinModel) -> BeerFullModel:
    async with in_transaction() as connection:
        beer = beer.dict(exclude_unset=True)
        beer_db = await Beer.create(**beer, using_db=connection)
    response.status_code = status.HTTP_201_CREATED
    return beer_db


@beer_router.put('/{beer_id}',
                 responses={200: {'model': BeerFullModel},
                            201: {'model': BeerFullModel}})
async def change_beer(response: Response, beer_id: Annotated[int, Path()], beer: BeerMinModel) -> BeerFullModel:
    async with in_transaction() as connection:
        beer_created = await Beer.update_or_create(defaults=beer.dict(), id=beer_id,
                                                   using_db=connection)
        if beer_created[1]:
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_200_OK
        return beer_created[0]


@beer_router.patch('/{beer_id}',
                   responses={200: {'model': BeerFullModel},
                              404: {'model': BadBeerError}})
async def edit_beer(response: Response, beer_id: Annotated[int, Path()], beer: BeerMinModel) -> BeerFullModel:
    async with in_transaction() as connection:
        if beer_db := await Beer.get_or_none(id=beer_id, using_db=connection):
            await beer_db.update_from_dict(beer.dict(exclude_unset=True))
            await beer_db.save()
            response.status_code = status.HTTP_200_OK
            return beer_db
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadBeerError)


@beer_router.delete('/{beer_id}',
                    responses={204: {'model': None},
                               404: {'model': BadBeerError}})
async def delete_beer(response: Response, beer_id: Annotated[int, Path()]) -> None:
    async with in_transaction() as connection:
        if beer := await Beer.get_or_none(id=beer_id, using_db=connection):
            await beer.delete(using_db=connection)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Beer not found')
