from logging import getLogger
from typing import Optional

from interactions import User, Member, Guild, MISSING
from interactions.client.errors import Forbidden
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from apis import get_minecraft_profile, get_hypixel_discord_link, get_catacombs_levels, get_minecraft_name
from discordclient import DiscordClient
from failures import *
from model import Player, LinkedRole

_logger = getLogger(__name__)


async def link_account(minecraft_name: str, discord_user: User):
    _logger.info(f'Linking {discord_user.username} to {minecraft_name}')

    minecraft_uuid, minecraft_name = await get_minecraft_profile(minecraft_name)
    hypixel_discord_link = await get_hypixel_discord_link(minecraft_uuid)

    if discord_user.username != hypixel_discord_link:
        raise WrongDiscordUsernameLinked

    discord_id_str = str(discord_user.id)

    async with in_transaction():
        await Player.filter(Q(discord_id=discord_id_str) | Q(minecraft_uuid=minecraft_uuid)).delete()
        player = await Player.create(minecraft_uuid=minecraft_uuid, discord_id=discord_id_str, catacombs_level=0)

    await update_guild_members(player=player)


async def unlink_account(discord_user: User):
    _logger.info(f'Unlinking {discord_user.id}')

    discord_id_str = str(discord_user.id)

    async with in_transaction():
        if not await Player.exists(discord_id=discord_id_str):
            raise NotLinked

        await Player.filter(discord_id=discord_id_str).delete()

    await clear_discord_user(discord_user)


async def update_guild_members(guild: Guild = None, player: Player = None):
    _logger.info(f'Updating guild members, filtering {guild=} {player=}')

    guilds = [guild] if guild else DiscordClient.guilds
    players = [player] if player else await Player.all()

    guild_roles_dict = await _get_guild_roles_dict(guilds)

    for player in players:
        await _update_catacombs_level(player.minecraft_uuid)
        nickname = await _get_nickname(player.discord_id)

        for guild, role_id in guild_roles_dict.items():
            _logger.debug(f'HERE: {guild.name=} {role_id=}')
            member = guild.get_member(player.discord_id)
            await _update_member(member, nickname, role_id)


async def clear_discord_user(discord_user: User):
    _logger.info(f'Clearing user {discord_user.id}')

    for guild in discord_user.mutual_guilds:
        member = guild.get_member(discord_user.id)
        await member.edit_nickname(new_nickname=MISSING)

        linked_role = await LinkedRole.get_or_none(guild_id=guild.id)
        if linked_role is not None:
            await member.remove_role(linked_role.role_id)


async def set_linked_role(guild: Guild, role_id: int):
    _logger.info(f'Setting linked role for {guild=} to {role_id=}')

    await LinkedRole.update_or_create(guild_id=guild.id, role_id=role_id)
    await update_guild_members(guild=guild)


async def remove_linked_role(guild: Guild):
    _logger.info(f'Removing linked role for {guild=}')
    await LinkedRole.filter(guild_id=guild.id).delete()


async def _update_catacombs_level(minecraft_uuid):
    _logger.debug(f'Refreshing catacombs level for {minecraft_uuid=}')

    current_level = max(await get_catacombs_levels(minecraft_uuid))
    await Player.filter(minecraft_uuid=str(minecraft_uuid)).update(catacombs_level=current_level)


async def _update_member(member: Optional[Member], nickname: str, linked_role_id: int):
    if member is None:
        return

    _logger.debug(f'Updating {member.id=} with {nickname=}, {linked_role_id=}')

    try:
        await member.edit_nickname(nickname)
        if linked_role_id is not None:
            await member.add_role(linked_role_id)

    except Forbidden as e:
        _logger.error(f'Error updating {member.username}: {e}')  # TODO hide username, add error messages etc


async def _get_guild_roles_dict(guilds: list[Guild]) -> dict[Guild, int]:
    _logger.info(f'Getting guild roles dict for {len(guilds)} guilds')

    linked_roles = await LinkedRole.filter(guild_id__in=[g.id for g in guilds])

    guild_roles_dict = {}
    for guild in guilds:
        linked_role = next((role for role in linked_roles if role.guild_id == guild.id), None)
        role_id = linked_role.role_id if linked_role else None

        guild_roles_dict[guild] = role_id

    return guild_roles_dict
    # Replace with prettier code if any is found


async def _get_nickname(discord_user_id: int) -> str:
    _logger.debug(f'Getting nickname for {discord_user_id=}')

    db_player = await Player.get_or_none(discord_id=str(discord_user_id))
    actual_name = await get_minecraft_name(db_player.minecraft_uuid)
    catacombs_level = round(db_player.catacombs_level, 2)

    nickname = f'{actual_name} [{catacombs_level}]'  # TODO externalise format
    return nickname
