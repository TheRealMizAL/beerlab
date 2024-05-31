from tortoise import Model, fields
from tortoise.validators import MinValueValidator
from tortoise.functions import Avg

from core.db.validators import BeforeTodayValidator
from .city import City
from .reviews import Review


class Manufacturer(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, null=False)
    year_of_creation = fields.IntField(null=False, validators=[MinValueValidator(1970), BeforeTodayValidator()])
    city: fields.ForeignKeyRelation["City"] = fields.ForeignKeyField('main.City',
                                                                     null=True, on_delete=fields.SET_NULL,
                                                                     on_update=fields.CASCADE)

    beers: fields.ReverseRelation["Beer"]

    class Meta:
        table = "manufacturers"


class Beer(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, null=False)
    style = fields.CharField(max_length=255, null=True)
    abv = fields.FloatField(null=True)
    plato = fields.FloatField(null=True)
    ibu = fields.FloatField(null=True)

    manufacturer: fields.ForeignKeyRelation["Manufacturer"] = fields.ForeignKeyField('main.Manufacturer',
                                                                                     null=True,
                                                                                     on_delete=fields.SET_NULL,
                                                                                     on_update=fields.CASCADE,
                                                                                     related_name='beers')
    reviews: fields.ReverseRelation["Review"]

    @property
    async def avg_rating(self):
        return await self.reviews.all().annotate(avg_score=Avg("rating"))
