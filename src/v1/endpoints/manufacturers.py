from typing import Annotated

from core.schemas.manufacturers import ManufacturerFullModel, ManufacturerMinModel
from fastapi import APIRouter, Path, HTTPException, status, Response
from tortoise.transactions import in_transaction

from core.db.models import Manufacturer
from core.schemas.errors import BadManufacturerError

manufacturer_router = APIRouter(prefix='/manufacturer',
                                tags=['Manufacturer'])


@manufacturer_router.get('/{manufacturer_id}',
                         responses={200: {'model': ManufacturerFullModel},
                                    404: {'model': BadManufacturerError}})
async def get_manufacturer(manufacturer_id: Annotated[int, Path()]) -> ManufacturerFullModel:
    async with in_transaction() as connection:
        if manufacturer := await Manufacturer.get_or_none(id=manufacturer_id, using_db=connection):
            return manufacturer
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadManufacturerError)


@manufacturer_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_manufacturer(response: Response, manufacturer: ManufacturerMinModel) -> ManufacturerFullModel:
    async with in_transaction() as connection:
        manufacturer = manufacturer.dict(exclude_unset=True)
        manufacturer_db = await Manufacturer.create(**manufacturer, using_db=connection)
    response.status_code = status.HTTP_201_CREATED
    return manufacturer_db


@manufacturer_router.put('/{manufacturer_id}',
                         responses={200: {'model': ManufacturerFullModel},
                                    201: {'model': ManufacturerFullModel}})
async def change_manufacturer(response: Response, manufacturer_id: Annotated[int, Path()],
                              manufacturer: ManufacturerMinModel) -> ManufacturerFullModel:
    async with in_transaction() as connection:
        manufacturer_created = await Manufacturer.update_or_create(defaults=manufacturer.dict(), id=manufacturer_id,
                                                                   using_db=connection)
        if manufacturer_created[1]:
            response.status_code = status.HTTP_201_CREATED
        else:
            response.status_code = status.HTTP_200_OK
        return manufacturer_created[0]


@manufacturer_router.patch('/{manufacturer_id}',
                           responses={200: {'model': ManufacturerFullModel},
                                      404: {'model': BadManufacturerError}})
async def edit_manufacturer(response: Response, manufacturer_id: Annotated[int, Path()],
                            manufacturer: ManufacturerMinModel) -> ManufacturerFullModel:
    async with in_transaction() as connection:
        if manufacturer_db := await Manufacturer.get_or_none(id=manufacturer_id, using_db=connection):
            await manufacturer_db.update_from_dict(manufacturer.dict(exclude_unset=True))
            await manufacturer_db.save()
            response.status_code = status.HTTP_200_OK
            return manufacturer_db
        raise HTTPException(status.HTTP_404_NOT_FOUND, BadManufacturerError)


@manufacturer_router.delete('/{manufacturer_id}',
                            responses={204: {'model': None},
                                       404: {'model': BadManufacturerError}})
async def delete_manufacturer(response: Response, manufacturer_id: Annotated[int, Path()]) -> None:
    async with in_transaction() as connection:
        if manufacturer := await Manufacturer.get_or_none(id=manufacturer_id, using_db=connection):
            await manufacturer.delete(using_db=connection)
            response.status_code = status.HTTP_204_NO_CONTENT
            return
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Manufacturer not found')
