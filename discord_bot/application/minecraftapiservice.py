from logging import getLogger
from uuid import UUID

from httpx import AsyncClient, HTTPStatusError, RequestError

from discord_bot.application.failure import UnknownMinecraftUsername, MinecraftAPIRequestFailed


class MinecraftAPIService:
    _log = getLogger(__name__)

    def __init__(self):
        self._log.debug("Initialising")

        self._api_client = AsyncClient(base_url="https://api.minecraftservices.com")

    async def get_minecraft_profile(self, name: str) -> (UUID, str):
        self._log.debug(f"Getting Minecraft profile for {name}")

        try:
            response = await self._api_client.get(f"/minecraft/profile/lookup/name/{name}")
            response.raise_for_status()

            uuid = UUID(response.json()["id"])
            actual_name = response.json()["name"]
            return uuid, actual_name

        except HTTPStatusError as e:
            self._log.error(f"{e}")
            raise UnknownMinecraftUsername

        except RequestError as e:
            self._log.warning("Request failed", exc_info=e)
            raise MinecraftAPIRequestFailed from e

    async def get_minecraft_name(self, uuid: UUID) -> str:
        self._log.debug(f"Getting Minecraft name for {uuid}")

        try:
            response = await self._api_client.get(f"/minecraft/profile/lookup/{uuid}")
            response.raise_for_status()

            name = response.json()["name"]
            return name

        except RequestError as e:
            self._log.warning("Request failed", exc_info=e)
            raise MinecraftAPIRequestFailed from e
