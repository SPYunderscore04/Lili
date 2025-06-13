from logging import getLogger
from uuid import UUID

from interactions import Member
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from discord_bot.application.failure import DiscordTagMismatch, NotLinked
from discord_bot.application.hypixelapiservice import HypixelAPIService
from discord_bot.application.memberupdateservice import MemberUpdateService
from discord_bot.application.minecraftapiservice import MinecraftAPIService
from discord_bot.persistence.link import Link


class LinkingService:
    _log = getLogger(__name__)

    def __init__(
        self,
        minecraft_api: MinecraftAPIService,
        hypixel_api: HypixelAPIService,
        member_update_service: MemberUpdateService,
    ):
        self._log.debug("Initialising")

        self._minecraft_api = minecraft_api
        self._hypixel_api = hypixel_api
        self._member_update_service = member_update_service

    async def link_member(self, member: Member, minecraft_name: str) -> None:
        self._log.info(f"Linking @{member.username} to {minecraft_name}")

        uuid, _ = await self._minecraft_api.get_minecraft_profile(minecraft_name)
        discord_tag = await self._hypixel_api.get_linked_discord_tag(uuid)
        if member.username != discord_tag:
            raise DiscordTagMismatch

        async with Link.id_lock.lock(member.id):
            await self._create_link(member.id, uuid)
            await self._member_update_service.update_member(member)

    async def link_member_without_checks(self, member: Member, minecraft_name: str) -> None:
        self._log.info(f"Linking @{member.username} to {minecraft_name} without checks")

        uuid, _ = await self._minecraft_api.get_minecraft_profile(minecraft_name)

        async with Link.id_lock.lock(member.id):
            await self._create_link(member.id, uuid)
            await self._member_update_service.update_member(member)

    async def unlink_member(self, member: Member) -> None:
        self._log.info(f"Unlinking @{member.username}")

        if not await Link.exists(discord_id=member.id):
            raise NotLinked

        async with Link.id_lock.lock(member.id):
            await self._delete_link(member.id)
            await self._member_update_service.clean_member(member)

    async def _create_link(self, discord_id: int, minecraft_uuid: UUID) -> None:
        self._log.debug(f"Creating link: {discord_id=} to {minecraft_uuid=}")

        async with in_transaction():
            await Link.filter(Q(discord_id=discord_id) | Q(minecraft_uuid=minecraft_uuid)).delete()
            await Link.create(minecraft_uuid=minecraft_uuid, discord_id=discord_id)

    async def _delete_link(self, discord_id: int) -> None:
        self._log.debug(f"Deleting link for {discord_id=}")

        async with in_transaction():
            await Link.filter(discord_id=discord_id).delete()
