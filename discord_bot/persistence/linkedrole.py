from tortoise.models import Model
from tortoise.fields import *


class LinkedRole(Model):
    guild_id = DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    role_id = DecimalField(max_digits=20, decimal_places=0)
