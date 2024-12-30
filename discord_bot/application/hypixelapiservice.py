from logging import getLogger
from uuid import UUID

from httpx import AsyncClient, RequestError

from discord_bot.application.failure import HypixelAPIRequestFailed, NoDiscordTagLinked


class HypixelAPIService:
    _log = getLogger(__name__)

    def __init__(self, api_key: str):
        self._log.debug("Initialising")

        self._client = AsyncClient(base_url="https://api.hypixel.net/v2", headers={"API-Key": api_key})

    async def get_linked_discord_tag(self, uuid: UUID) -> str:
        self._log.debug(f"Getting linked Discord tag for {uuid}")

        try:
            response = await self._client.get(f"/player?uuid={uuid}")
            response.raise_for_status()

            discord_name = response.json()["player"]["socialMedia"]["links"]["DISCORD"]
            return discord_name

        except (KeyError, TypeError):
            raise NoDiscordTagLinked

        except RequestError as e:
            self._log.warning("Request failed", exc_info=e)
            raise HypixelAPIRequestFailed from e

    async def get_catacombs_level(self, uuid: UUID) -> float:
        self._log.debug(f"Getting Catacombs level for {uuid}")

        xp_list = await self.get_catacombs_experiences(uuid)
        if len(xp_list) == 0:
            return 0

        levels = (self._calculate_catacombs_level(xp) for xp in xp_list)
        return max(levels)

    async def get_catacombs_experiences(self, uuid: UUID) -> list[int]:
        self._log.debug(f"Getting Catacombs experiences for {uuid}")

        try:
            response = await self._client.get(f"/skyblock/profiles?uuid={uuid}")
            response.raise_for_status()

            profiles = response.json()["profiles"]

            xp_list = []
            for profile in profiles:
                try:
                    xp = profile["members"][uuid.hex]["dungeons"]["dungeon_types"]["catacombs"]["experience"]
                    xp_list.append(xp)
                except KeyError:
                    pass

            return xp_list

        except RequestError as e:
            self._log.warning("Request failed", exc_info=e)
            raise HypixelAPIRequestFailed from e

    @staticmethod
    def _calculate_catacombs_level(experience: float) -> float:
        level = 0
        for next_lvl_xp in HypixelAPIService._cata_xp_to_next_level():
            if experience < next_lvl_xp:
                return level + experience / next_lvl_xp

            level += 1
            experience -= next_lvl_xp

    @staticmethod
    def _cata_xp_to_next_level():
        xp_required = [
            50,
            75,
            110,
            160,
            230,
            330,
            470,
            670,
            950,
            1340,
            1890,
            2665,
            3760,
            5260,
            7380,
            10300,
            14400,
            20000,
            27600,
            38000,
            52500,
            71500,
            97000,
            132000,
            180000,
            243000,
            328000,
            445000,
            600000,
            800000,
            1065000,
            1410000,
            1900000,
            2500000,
            3300000,
            4300000,
            5600000,
            7200000,
            9200000,
            12000000,
            15000000,
            19000000,
            24000000,
            30000000,
            38000000,
            48000000,
            60000000,
            75000000,
            93000000,
            116250000,
        ]

        # Levels 0-50
        for xp in xp_required:
            yield xp

        # Levels 51+
        while True:
            yield 200000000
