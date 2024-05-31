from pydantic import ConfigDict
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from core.db.models import Manufacturer

manufacturer_full_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "BrewDog",
                    "year_of_creation": 2007,
                    "city_id": 1
                }
            ]
        }
)

manufacturer_min_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "BrewDog",
                    "year_of_creation": 2007,
                    "city_id": 1
                }
            ]
        }
)

Tortoise.init_models(["core.db.models.city"], app_label="main")
ManufacturerFullModel = pydantic_model_creator(Manufacturer, exclude_readonly=False, exclude=("beers", "city",),
                                               optional=("city_id",),
                                               name="ManufacturerFullModel", model_config=manufacturer_full_model_config)
ManufacturerMinModel = pydantic_model_creator(Manufacturer, exclude_readonly=True,
                                              optional=("city_id",),
                                              name="ManufacturerMinModel", model_config=manufacturer_min_config)
