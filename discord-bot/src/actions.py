from logging import getLogger

from interactions import Client, User, Member
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from apis import get_minecraft_profile, get_hypixel_discord_link
from model import Player
from failures import *

_logger = getLogger(__name__)


async def link_account(minecraft_name: str, discord_user: User | Member):
    _logger.info(f'Linking {discord_user.username} to {minecraft_name}')

    minecraft_uuid, minecraft_name = await get_minecraft_profile(minecraft_name)
    hypixel_discord_link = await get_hypixel_discord_link(minecraft_uuid)

    if discord_user.username != hypixel_discord_link:
        raise WrongDiscordUsernameLinked

    discord_id_str = str(discord_user.id)

    async with in_transaction():
        await Player.filter(Q(discord_id=discord_id_str) | Q(minecraft_uuid=minecraft_uuid)).delete()
        await Player.create(minecraft_uuid=minecraft_uuid,
                            discord_id=discord_id_str,
                            catacombs_level=0)

    # TODO refresh cata level, nick, roles


async def unlink_account(discord_user_id: int):
    _logger.info(f'Unlinking {discord_user_id}')

    discord_id_str = str(discord_user_id)

    async with in_transaction():
        if not await Player.exists(discord_id=discord_id_str):
            raise NotLinked

        await Player.filter(discord_id=discord_id_str).delete()

    # TODO unset nick, roles


async def set_linked_role(guild_id: int, role_id: int):
    _logger.info(f'Setting linked role in {guild_id} to {role_id}')
    raise NotImplementedError


async def remove_linked_role(guild_id: int):
    _logger.info(f'Unsetting linked role in {guild_id}')
    raise NotImplementedError


async def add_level_role(guild_id: int, role_id: int, level: float):
    _logger.info(f'Setting role {role_id} for level {level} in {guild_id}')
    raise NotImplementedError


async def remove_level_role(guild_id: int, role_id: int):
    _logger.info(f'Removing role {role_id} in {guild_id}')
    raise NotImplementedError


async def clear_level_roles(guild_id: int):
    _logger.info(f'Clearing level roles in {guild_id}')
    raise NotImplementedError


async def update_member_roles(client: Client, guild_id: int):
    _logger.info(f'Updating roles in {guild_id}')
    await update_linked_roles(client, guild_id)
    await update_level_roles(client, guild_id)


async def update_linked_roles(client: Client, guild_id: int):
    _logger.info(f'Updating linked roles in {guild_id}')
    raise NotImplementedError


async def update_level_roles(client: Client, guild_id: int):
    _logger.info(f'Updating level roles in {guild_id}')
    raise NotImplementedError


async def update_nicknames(client: Client):
    _logger.info(f'Updating nicknames')
    raise NotImplementedError
