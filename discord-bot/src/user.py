from tortoise.fields import UUIDField, CharField, FloatField
from tortoise.models import Model


class User(Model):
    minecraft_uuid = UUIDField(primary_key=True)
    discord_username = CharField(max_length=32, unique=True, db_index=True)
    catacombs_level = FloatField()
