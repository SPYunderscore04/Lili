from tortoise import Model
from tortoise.fields import *


class Player(Model):
    minecraft_uuid = UUIDField(unique=True, db_index=True)
    discord_id = DecimalField(unique=True, db_index=True, max_digits=20, decimal_places=0)
    last_updated = DatetimeField(null=True, db_index=True)
