from tortoise import Model, fields


class City(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255, null=False)

    class Meta:
        table = "cities"
