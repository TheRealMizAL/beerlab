from tortoise import Model, fields

from .reviews import Review


class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=20, null=True)
    first_name = fields.CharField(max_length=255, null=False)
    last_name = fields.CharField(max_length=255, null=True)

    birthday = fields.DateField(null=True)
    reg_date = fields.DatetimeField(null=False, auto_now_add=True)

    creds: fields.BackwardOneToOneRelation["Creds"]
    reviews: fields.ReverseRelation["Review"]

    @property
    async def link(self):
        if self.username:
            return f"@{self.username}"
        return f"@id{self.id}"

    async def get_full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    class PydanticMeta:
        exclude = ("creds", )


class Creds(Model):
    login = fields.CharField(max_length=255, null=False)
    passwd = fields.CharField(max_length=60, null=False)
    user: fields.OneToOneRelation["User"] = fields.OneToOneField('main.User', 'creds', primary_key=True)
