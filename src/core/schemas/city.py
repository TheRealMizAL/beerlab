from pydantic import ConfigDict
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from core.db.models import City

city_full_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Е-град"
                }
            ]
        }
)

city_min_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Е-град"
                }
            ]
        }
)

Tortoise.init_models(["core.db.models.city"], app_label="main")
CityFullModel = pydantic_model_creator(City, exclude_readonly=False, name='CityFullModel', exclude=('manufacturerss',),
                                       model_config=city_full_model_config)
CityMinModel = pydantic_model_creator(City, exclude_readonly=True, name='CityMinModel',
                                      model_config=city_min_model_config)
