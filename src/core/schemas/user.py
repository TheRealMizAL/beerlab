from datetime import datetime, date

from pydantic import ConfigDict
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from core.db.models import User
from utils.random_data_generator import random_date

user_full_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "username": "aboba",
                    "first_name": "Nill",
                    "last_name": "Kiggers",
                    "birthday": random_date(date(1970, 1, 1)),
                    "reg_date": datetime.now(),
                }
            ]
        }
)

user_min_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "username": "aboba",
                    "first_name": "Nill",
                    "last_name": "Kiggers",
                    "birthday": random_date(date(1970, 1, 1)),
                }
            ]
        }
)

Tortoise.init_models(["core.db.models.user"], app_label="main")
UserFullModel = pydantic_model_creator(User, exclude_readonly=False, name="UserFullModel",
                                       exclude=("reviews", "reg_date"), model_config=user_full_model_config)
UserMinModel = pydantic_model_creator(User, exclude_readonly=True, name="UserMinModel",
                                      exclude=("reviews", "reg_date"), model_config=user_min_model_config)


class UserRegisterModel(UserMinModel):
    model_config = ConfigDict(
            json_schema_extra={
                "examples": [
                    {
                        "username": "aboba",
                        "first_name": "Nill",
                        "last_name": "Kiggers",
                        "birthday": random_date(date(1970, 1, 1)),
                        "password": "passwd"
                    }
                ]
            },
            title="UserRegisterModel"
    )
    password: str
