from typing import Annotated

from fastapi import APIRouter, Path, Response, HTTPException, status
from tortoise.transactions import in_transaction

from core.db.models import City
from core.schemas.city import CityFullModel, CityMinModel
from core.schemas.errors import BadCityError

city_router = APIRouter(prefix='/city',
                        tags=['City'])


@city_router.get('/{city_id}',
                 responses={200: {'model': CityFullModel},
                            404: {'model': BadCityError}})
async def get_city(city_id: Annotated[int, Path()]) -> CityFullModel:
    async with in_transaction() as connection:
        if city := await City.get_or_none(id=city_id, using_db=connection):
            return city
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadCityError)


@city_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_city(response: Response, city: CityMinModel) -> CityFullModel:
    async with in_transaction() as connection:
        city = city.dict(exclude_unset=True)
        city_db = await City.create(**city, using_db=connection)
    response.status_code = status.HTTP_201_CREATED
    return city_db


@city_router.put('/{city_id}',
                 responses={200: {'model': CityFullModel},
                            201: {'model': CityFullModel}})
async def change_city(response: Response, city_id: Annotated[int, Path()], city: CityMinModel):
    async with in_transaction() as connection:
        city_created = await City.update_or_create(defaults=city.dict(), id=city_id, using_db=connection)
        if city_created[1]:
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_200_OK
        return city_created[0]


@city_router.patch('/{city_id}',
                   responses={200: {'model': CityFullModel},
                              404: {'model': BadCityError}})
async def edit_city(response: Response, city_id: Annotated[int, Path()], city: CityMinModel):
    async with in_transaction() as connection:
        if city_db := await City.get_or_none(id=city_id, using_db=connection):
            await city_db.update_from_dict(city.dict(exclude_unset=True))
            await city_db.save(using_db=connection)
            response.status_code = status.HTTP_200_OK
            return city_db
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadCityError)


@city_router.delete('/{city_id}',
                    responses={204: {'model': None},
                               404: {'model': BadCityError}})
async def delete_city(response: Response, city_id: Annotated[int, Path()]):
    async with in_transaction() as connection:
        if city := await City.get_or_none(id=city_id, using_db=connection):
            await city.delete(using_db=connection)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadCityError)
