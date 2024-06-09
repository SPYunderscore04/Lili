from logging import getLogger

from interactions import Client


_logger = getLogger(__name__)


async def link_account(minecraft_name: str, discord_user_id: int):
    _logger.info(f'Linking {discord_user_id} to {minecraft_name}')
    raise NotImplementedError
    # Resolve Mojang UUID
    # Check if link exists on Hypixel
    # Unlink old Discord account if necessary
    # Unlink old Minecraft account if necessary
    # Link accounts


async def unlink_account(discord_user_id: int):
    _logger.info(f'Unlinking {discord_user_id}')
    raise NotImplementedError
    # Check if discord account is linked
    # Unlink account


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
