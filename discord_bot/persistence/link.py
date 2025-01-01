from tortoise import Model
from tortoise.fields import *

from discord_bot.util.valuelock import ValueLock


class Link(Model):
    discord_id = DecimalField(unique=True, db_index=True, max_digits=20, decimal_places=0)
    minecraft_uuid = UUIDField(unique=True, db_index=True)
    last_nickname_update = DatetimeField(null=True, db_index=True)

    id_lock = ValueLock[int]()
