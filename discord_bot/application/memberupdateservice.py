from logging import getLogger
from typing import Optional

from interactions import Member, Guild, Role, Client
from interactions.client.errors import HTTPException as DiscordHTTPException
from tortoise.timezone import now

from discord_bot.application.failure import MemberUpdateFailed
from discord_bot.application.hypixelapiservice import HypixelAPIService
from discord_bot.application.minecraftapiservice import MinecraftAPIService
from discord_bot.persistence.link import Link


class MemberUpdateService:
    _log = getLogger(__name__)

    def __init__(
        self,
        minecraft_api: MinecraftAPIService,
        hypixel_api: HypixelAPIService,
        discord_client: Client,
    ):
        self._log.debug("Initialising")

        self._minecraft_api = minecraft_api
        self._hypixel_api = hypixel_api
        self._discord_client = discord_client

    async def update_most_due_member(self) -> None:
        self._log.info("Updating most due member")

        async with Link.id_lock.lock_all() as lock:
            link = await Link.all().order_by("last_nickname_update").first()
            if link is None:
                self._log.debug("No links to update nicknames for")
                return

            await lock.downgrade(link.discord_id)

            members = await self._get_memberships_for_discord_user(link.discord_id)
            if members is None:
                self._log.info(f"No memberships for {link} found, deleting link")
                await link.delete()
                return

            for member in members:
                try:
                    await self.update_member(member)
                except MemberUpdateFailed:
                    self._log.info(f"Could not update @{member.username} in {member.guild.name} (guild owner?)")
                    # A bot can never set the nickname of the guild owner

    async def update_member(self, member: Member) -> None:
        self._log.debug(f"Updating @{member.username}")

        link = await Link.get(discord_id=member.id)

        link.last_nickname_update = now()
        await link.save()

        name = await self._minecraft_api.get_minecraft_name(link.minecraft_uuid)
        level = await self._hypixel_api.get_catacombs_level(link.minecraft_uuid)

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
        await member.edit_nickname()  # Remove nickname

    async def _get_memberships_for_discord_user(self, discord_id: int) -> Optional[list[Member]]:
        self._log.debug(f"Getting memberships for {discord_id=}")

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
