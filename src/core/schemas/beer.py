from pydantic import ConfigDict
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from core.db.models import Beer

beer_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Tactical Nuclear Penguin",
                    "style": "lager",
                    "abv": 32,
                    "ibu": 90,
                    "plato": 7,
                    "manufacturer_id": 1
                }
            ]
        },
)

beer_min_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Tactical Nuclear Penguin",
                    "style": "lager",
                    "abv": 32,
                    "ibu": 90,
                    "plato": 7,
                    "manufacturer_id": 1
                }
            ]
        },
)

Tortoise.init_models(["core.db.models"], app_label="main")
BeerMaxModel = pydantic_model_creator(Beer, exclude_readonly=False, name='BeerMaxModel')
BeerFullModel = pydantic_model_creator(Beer, exclude_readonly=False,
                                       exclude=('reviews', 'manufacturer'),
                                       optional=('abv', 'ibu', 'manufacturer_id', 'plato',),
                                       name='BeerFullModel', model_config=beer_model_config)
BeerMinModel = pydantic_model_creator(Beer, exclude_readonly=True,
                                      optional=('abv', 'ibu', 'manufacturer_id', 'plato',),
                                      name='BeerMinModel', model_config=beer_min_model_config)
