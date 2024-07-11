from tortoise.fields import *
from tortoise.models import Model


class Player(Model):
    minecraft_uuid = UUIDField(unique=True, db_index=True)
    discord_id = DecimalField(unique=True, db_index=True, max_digits=20, decimal_places=0)
    catacombs_level = FloatField()


class LinkedRole(Model):
    guild_id = DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    role_id = DecimalField(max_digits=20, decimal_places=0)
