from datetime import date

from tortoise.exceptions import ValidationError
from tortoise.validators import Validator


class BeforeTodayValidator(Validator):

    def __call__(self, value: int):
        if value > date.today().year:
            raise ValidationError
