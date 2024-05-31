from pydantic import ConfigDict
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from core.db.models import Review

review_full_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "review": "5/5 no drama",
                    "rating": 5,
                    "beer_id": 1,
                    "user_id": 1
                }
            ]
        }
)
review_min_model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "review": "5/5 no drama",
                    "rating": 5,
                    "beer_id": 1,
                    "user_id": 1
                }
            ]
        }
)

Tortoise.init_models(["core.db.models"], app_label="main")
ReviewFullModel = pydantic_model_creator(Review, exclude_readonly=False, name="ReviewFullModel",
                                         exclude=("beer", "user",), model_config=review_full_model_config)
ReviewMinModel = pydantic_model_creator(Review, exclude_readonly=True, name="ReviewMinModel",
                                        exclude=("beer", "user",), model_config=review_min_model_config)
