from tortoise import Model, fields
from tortoise.validators import MaxValueValidator, MinValueValidator


class Review(Model):
    id = fields.IntField(primary_key=True)
    review = fields.TextField(null=True)
    rating = fields.IntField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])

    beer = fields.ForeignKeyField('main.Beer', 'reviews',
                                  null=False, on_delete=fields.CASCADE)
    user = fields.ForeignKeyField('main.User', 'reviews',
                                  null=False, on_delete=fields.CASCADE)
