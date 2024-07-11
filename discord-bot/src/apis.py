from logging import getLogger
from uuid import UUID

from httpx import AsyncClient, RequestError, HTTPStatusError

from environment import Environment
from failures import *
from util import calculate_catacombs_level

_logger = getLogger(__name__)
_mojang_api_client = AsyncClient(base_url='https://api.mojang.com')
_mojang_sessionserver_client = AsyncClient(base_url='https://sessionserver.mojang.com')  # wtf mojang
_hypixel_api_client = AsyncClient(base_url='https://api.hypixel.net/v2',
                                  headers={'API-Key': Environment.HYPIXEL_API_KEY})


async def get_minecraft_profile(minecraft_name: str) -> (UUID, str):
    _logger.info(f'Getting Minecraft profile for {minecraft_name}')

    try:
        response = await _mojang_api_client.get(f'/users/profiles/minecraft/{minecraft_name}')
        response.raise_for_status()

        uuid = UUID(response.json()['id'])
        actual_name = response.json()['name']
        return uuid, actual_name

    except HTTPStatusError:
        raise UnknownMinecraftUsername

    except RequestError as e:
        raise MojangApiRequestFailed from e


async def get_minecraft_name(player_uuid: UUID) -> str:
    _logger.info(f'Getting Minecraft name for {player_uuid}')

    try:
        response = await _mojang_sessionserver_client.get(f'/session/minecraft/profile/{player_uuid}')
        response.raise_for_status()

        name = response.json()['name']
        return name

    except RequestError as e:
        raise MojangApiRequestFailed from e


async def get_hypixel_discord_link(player_uuid: UUID) -> str:
    _logger.info(f'Getting linked Discord name for {player_uuid}')

    try:
        response = await _hypixel_api_client.get(f'/player?uuid={player_uuid}')
        response.raise_for_status()

        discord_name = response.json()['player']['socialMedia']['links']['DISCORD']
        return discord_name

    except TypeError:
        raise NoDiscordUsernameLinked

    except RequestError as e:
        raise HypixelApiRequestFailed from e


async def get_catacombs_levels(player_uuid: UUID) -> list[float]:
    _logger.info(f'Getting Catacombs levels for {player_uuid}')

    try:
        response = await _hypixel_api_client.get(f'/skyblock/profiles?uuid={player_uuid}')
        response.raise_for_status()

        profiles = response.json()['profiles']

        xp_list = []
        for profile in profiles:
            try:
                xp = profile['members'][player_uuid.hex]['dungeons']['dungeon_types']['catacombs']['experience']
                xp_list.append(xp)
            except KeyError:
                pass

        catacombs_levels = [calculate_catacombs_level(xp) for xp in xp_list]
        return catacombs_levels

    except RequestError as e:
        raise HypixelApiRequestFailed from e
