from asyncio import sleep
from logging import getLogger
from typing import Optional

from interactions import Member, MISSING, Guild, Role, Client
from interactions.client.errors import HTTPException as DiscordHTTPException
from tortoise.timezone import now

from discord_bot.application.failure import MemberUpdateFailed
from discord_bot.application.hypixelapiservice import HypixelAPIService
from discord_bot.application.mojangapiservice import MojangAPIService
from discord_bot.persistence.player import Player


class MemberUpdateService:
    _log = getLogger(__name__)

    def __init__(self, mojang_api: MojangAPIService, hypixel_api: HypixelAPIService, discord_client: Client):
        self._log.debug("Initialising")

        self._mojang_api = mojang_api
        self._hypixel_api = hypixel_api
        self._discord_client = discord_client

        self._update_cooldown_sec = 60  # TODO calc from api limits

    async def run_update_loop(self) -> None:
        self._log.info("Starting update loop")

        while True:
            player = await Player.all().order_by("last_updated").first()
            if player is None:
                self._log.debug("No players to update")
                await sleep(self._update_cooldown_sec)
                continue

            members = await self._get_members_for_user(player.discord_id)
            if members is None:
                self._log.info(f"No memberships for {player} found, deleting link")
                await player.delete()
                continue

            for member in members:
                try:
                    await self.update_member(member)
                except MemberUpdateFailed:
                    self._log.info(f"Failed to update @{member.username} in {member.guild.name}")

            await sleep(self._update_cooldown_sec)

    async def update_member(self, member: Member) -> None:
        self._log.debug(f"Updating @{member.username}")

        player = await Player.get(discord_id=str(member.id))
        player.last_updated = now()
        await player.save()

        name = await self._mojang_api.get_minecraft_name(player.minecraft_uuid)
        level = await self._hypixel_api.get_catacombs_level(player.minecraft_uuid)

        nickname = self._format_nickname(name, level)
        verified_role = self._get_verified_role(member.guild)

        try:
            await member.edit_nickname(nickname)
            await member.add_role(verified_role)

        except DiscordHTTPException:
            raise MemberUpdateFailed(member, nickname, [verified_role])

    async def clean_member(self, member: Member) -> None:
        self._log.debug(f"Cleaning @{member.username}")

        verified_role = self._get_verified_role(member.guild)
        await member.remove_role(verified_role)
        await member.edit_nickname(MISSING)

    async def _get_members_for_user(self, discord_id: int) -> Optional[list[Member]]:
        self._log.debug(f"Getting members for {discord_id=}")

        # TODO check caching
        user = await self._discord_client.fetch_user(discord_id)
        if user is None:
            self._log.debug(f"Could not find user for {discord_id=}")
            return None

        guilds = user.mutual_guilds
        if len(guilds) == 0:
            self._log.debug(f"No mutual guilds with {discord_id=}")
            return None

        members = (g.get_member(discord_id) for g in guilds)
        members = list(filter(lambda m: m is not None, members))
        return members

    @staticmethod
    def _get_verified_role(guild: Guild) -> Role:
        return next(role for role in guild.roles if "verified" in role.name.lower())

    @staticmethod
    def _format_nickname(name: str, level: float) -> str:
        return f"{name} [{level:0.2f}]"
